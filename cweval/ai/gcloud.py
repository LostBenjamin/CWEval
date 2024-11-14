import os
import random
import time
from typing import Dict, List

import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account
from openai import OpenAI

from cweval.ai.openai import OpenAIClient


class GCloudClient(OpenAIClient):
    def __init__(
        self,
        model_name: str = 'meta/llama-3.1-405b-instruct-maas',
        rank: int = 0,
        cred_file: str = '',
        project_id: str = 'llm-malware-detection',
        model_location: str = "us-east5",
        base_url: str = "https://{MODEL_LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{MODEL_LOCATION}/endpoints/openapi/chat/completions?",
        token_cache_path: str = os.path.expanduser('~/.cache/gc_cred_token'),
        **kwargs,
    ) -> None:

        def read_cached_token() -> str:
            with open(token_cache_path, 'r') as f:
                token_time, token = f.read().strip().split(',', 1)
            token_time = float(token_time)
            assert time.time() - token_time < 45 * 60
            return token

        def refresh_token() -> str:
            cred = service_account.Credentials.from_service_account_file(
                cred_file,
                scopes=['https://www.googleapis.com/auth/cloud-platform'],
            )
            auth_request = google.auth.transport.requests.Request()
            cred.refresh(auth_request)
            token = cred.token
            with open(token_cache_path, 'w') as f:
                f.write(f'{int(time.time())},{token}')
            return token

        if rank == 0:
            token = refresh_token()
        else:
            for _ in range(60):
                try:
                    token = read_cached_token()
                    break
                except:
                    time.sleep(1)
            else:
                token = refresh_token()

        if 'meta/llama' in model_name:
            model_location = 'us-central1'

        self.client = OpenAI(
            api_key=token,
            base_url=base_url.format(
                MODEL_LOCATION=model_location, PROJECT_ID=project_id
            ),
            timeout=10
            * 60.0,  # https://github.com/openai/openai-python/blob/717e318d6e0c652721c6e7081acd6db226f77820/README.md?plain=1#L407
        )
        self.model_name = model_name
        self.kwargs = kwargs

    def send_message(
        self,
        messages: List[Dict[str, str]],
        **kwargs,
    ) -> List[str]:
        all_kwargs = self.kwargs.copy()
        all_kwargs.update(kwargs)
        n_samples = all_kwargs.pop('n', 1)
        resps: List[str] = []
        for _ in range(n_samples):
            comp = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **all_kwargs,
            )
            resps.append(''.join([c.message.content for c in comp.choices]))

        return resps
