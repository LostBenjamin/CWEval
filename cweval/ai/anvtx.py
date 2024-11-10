import os
import random
import time
from typing import List

import google.auth
import google.auth.transport.requests
from anthropic import AnthropicVertex
from detection.ai.openai import OpenAIClient
from google.oauth2 import service_account


class AnVtxClient(OpenAIClient):
    def __init__(
        self,
        model_name: str = 'claude-3-haiku@20240307',
        system_message: str | None = None,
        rank: int = 0,
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
        self.messages: List[str] = []
        if system_message:
            self.messages.append(
                {
                    "role": "system",
                    "content": system_message,
                }
            )
        self.kwargs = kwargs

    def send_message(
        self,
        content: str,
        stop: List[str] = None,
        retries: int = 1,
    ) -> str:
        msgs = self.messages + [
            {
                "role": "user",
                "content": content,
            },
        ]
        _sleep_time = 2
        for i in range(retries):
            try:
                msg = self.client.messages.create(
                    model=self.model_name,
                    messages=msgs,
                    stop_sequences=stop,
                    **self.kwargs,
                )
                out = ''.join([c.text for c in msg.content])
                self.messages = msgs + [
                    {
                        "role": "assistant",
                        "content": out,
                    },
                ]
                return out
            except Exception as e:
                import traceback

                traceback.print_exc()
                # from IPython import embed; embed()
                time.sleep(_sleep_time)
                _sleep_time = min(30 + random.randint(0, 8), 2 * _sleep_time)
        else:
            # print(f'[chat_send_msg] Failed to send_message')
            # from IPython import embed; embed()
            raise Exception('[send_message] Failed to send_message')
