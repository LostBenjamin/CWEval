from typing import Dict, List

import google.generativeai as genai

from cweval.ai import AIAPI


class GoogleAIClient(AIAPI):
    def __init__(
        self,
        api_key: str,
        model_name: str = 'gemini-1.5-flash-002',
        **kwargs,
    ) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)
        self.kwargs = kwargs

    def send_message(
        self,
        messages: List[Dict[str, str]],
        **kwargs,
    ) -> List[str]:
        # assert len(messages) == 1, f'{len(messages) = }'
        # content = messages[-1]['content']

        contents = [
            {
                'role': 'user' if m['role'] == 'user' else 'model',
                'parts': m['content'],
            }
            for m in messages
        ]

        all_kwargs = self.kwargs.copy()
        all_kwargs.update(kwargs)
        # openai kwargs to google gemini ones
        all_kwargs['max_output_tokens'] = all_kwargs.pop('max_completion_tokens', None)
        num_samples = all_kwargs.pop('n', None)
        resps = []
        for i in range(num_samples):
            print(f'{i = }', flush=True)
            resp = self._model.generate_content(
                contents=contents,
                generation_config={
                    **all_kwargs,
                    # 'stop_sequences': stop,
                    # 'temperature': 0.6,
                    # 'top_p': 0.9,
                    # 'top_k': 1,
                },
                safety_settings={
                    'sex': 'block_none',
                    'hate': 'block_none',
                    'harassment': 'block_none',
                    'danger': 'block_none',
                },
                request_options={"timeout": 2000},
            )
            resps.extend(
                [' '.join([p.text for p in c.content.parts]) for c in resp.candidates]
            )
        return resps

    def chat_send_message(
        self,
        messages: List[Dict[str, str]],
        **kwargs,
    ) -> str:
        raise NotImplementedError
        chat = self._model.start_chat(
            history=[
                {
                    'role': 'user' if m['role'] == 'user' else 'model',
                    'parts': m['content'],
                }
                for m in messages[:-1]
            ]
        )
        assert messages[-1]['role'] == 'user', f'{messages[-1] = }'
        content = messages[-1]['content']

        all_kwargs = self.kwargs.copy()
        all_kwargs.update(kwargs)
        # openai kwargs to google gemini ones
        all_kwargs['max_output_tokens'] = all_kwargs.pop('max_completion_tokens', None)
        all_kwargs['candidate_count'] = all_kwargs.pop('n', None)

        resp = chat.send_message(
            content=content,
            generation_config={
                **all_kwargs,
                # 'stop_sequences': stop,
                # 'temperature': 0.6,
                # 'top_p': 0.9,
                # 'top_k': 1,
            },
            safety_settings={
                'sex': 'block_none',
                'hate': 'block_none',
                'harassment': 'block_none',
                'danger': 'block_none',
            },
            request_options={"timeout": 2000},
        )
        return resp.text
