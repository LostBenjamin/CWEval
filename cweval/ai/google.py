import random
import time
from typing import Dict, List

import google.generativeai as genai
from detection.ai.base import AIAPI


class GoogleAIClient(AIAPI):
    def __init__(
        self,
        api_key: str,
        model_name: str = 'gemini-1.5-flash-001',
        system_message: str | None = None,
        **kwargs,
    ) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)
        self.chat = self._model.start_chat(
            history=[
                # {
                #     'role': 'user',
                #     'parts': ['You are an helpful expert in computer security.']
                # }
            ]
        )
        self.kwargs = kwargs

    def send_message(
        self,
        content: str,
        stop: List[str] = None,
        retries: int = 1,
    ) -> str:
        _sleep_time = 1
        for i in range(retries):
            try:
                response = self.chat.send_message(
                    content=content,
                    safety_settings={
                        'sex': 'block_none',
                        'hate': 'block_none',
                        'harassment': 'block_none',
                        'danger': 'block_none',
                    },
                    generation_config={
                        'stop_sequences': stop,
                        **self.kwargs,
                        # 'temperature': 0.6,
                        # 'top_p': 0.9,
                        # 'top_k': 1,
                    },
                    request_options={"timeout": 1000},
                )
                return response.text
            except Exception as e:
                import traceback

                traceback.print_exc()
                time.sleep(_sleep_time)
                _sleep_time = min(10 + random.random(), 2 * _sleep_time)
        else:
            # print(f'[chat_send_msg] Failed to send_message')
            # from IPython import embed; embed()
            raise Exception('[chat_send_msg] Failed to send_message')

    def clear_history(self) -> None:
        self.chat = self._model.start_chat(history=[])

    def history_str(self, roles: List[str] = []) -> str:
        return '\n\n\n'.join(
            f'>>>> role = {h.role} <<<<\n\n' + ''.join([p.text for p in h.parts])
            for h in self.chat.history
            if not roles or h.role in roles
        )

    @property
    def history_list(self) -> List[Dict[str, str]]:
        role_map = {
            'user': 'user',
            'model': 'assistant',
        }
        return [
            {
                'role': role_map[h.role],
                'content': ''.join([p.text for p in h.parts]),
            }
            for h in self.chat.history
        ]

    def edit_history(self, idx: int, content: str):
        try:
            assert len(self.chat.history[idx].parts) == 1
        except Exception as e:
            print(self.chat.history[idx].parts, flush=True)
            from IPython import embed

            embed()
        self.chat.history[idx].parts[0].text = content
