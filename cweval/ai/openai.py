from typing import Dict, List

from openai import OpenAI

from cweval.ai import AIAPI


class OpenAIClient(AIAPI):
    def __init__(
        self,
        api_key: str,
        model_name: str = 'gpt-4o-mini-2024-07-18',
        base_url: str | None = None,
        **kwargs,
    ) -> None:
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
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
        comp = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **all_kwargs,
        )
        return [c.message.content for c in comp.choices]
