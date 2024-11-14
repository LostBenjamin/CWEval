from typing import Dict, List

import google.auth
import google.auth.transport.requests
from anthropic import AnthropicVertex
from google.oauth2 import service_account

from cweval.ai.openai import OpenAIClient


class AnVtxClient(OpenAIClient):
    def __init__(
        self,
        model_name: str = 'claude-3-5-haiku@20241022',
        cred_file: str = '',
        project_id: str = 'llm-malware-detection',
        model_location: str = "us-east5",
        **kwargs,
    ) -> None:
        cred = service_account.Credentials.from_service_account_file(
            cred_file,
            scopes=['https://www.googleapis.com/auth/cloud-platform'],
        )

        self.client = AnthropicVertex(
            region=model_location,
            project_id=project_id,
            credentials=cred,
            timeout=10 * 60.0,
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
        # openai kwargs to this ones
        all_kwargs['max_tokens'] = all_kwargs.pop('max_completion_tokens', 4096)
        n_samples = all_kwargs.pop('n', 1)
        resps: List[str] = []
        for _ in range(n_samples):
            comp = self.client.messages.create(
                model=self.model_name,
                messages=messages,
                **all_kwargs,
            )
            resps.append(''.join([c.text for c in comp.content]))

        return resps
