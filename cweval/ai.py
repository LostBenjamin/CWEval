import abc
import os
import time
from typing import Dict, List

import together

client = together.Together()


class AIAPI(abc.ABC):

    def __init__(
        self,
        model: str,
        **kwargs,
    ) -> None:
        self.model = model
        self.req_kwargs = kwargs

    def send_message(self, messages: List[Dict[str, str]], **kwargs) -> List[str]:
        all_kwargs = self.req_kwargs.copy()
        all_kwargs.update(kwargs)
        if 'DeepSeek-R1' in self.model:
            all_kwargs['max_completion_tokens'] = 30000

        n_samples = all_kwargs.pop('n', 1)
        max_n_per_req: int = 10

        resp: List[str] = []
        for i, idx in enumerate(range(0, n_samples, max_n_per_req)):
            n_this = min(max_n_per_req, n_samples - i * max_n_per_req)
            if n_this > 1:
                all_kwargs['n'] = n_this
            else:
                all_kwargs.pop('n', 1)

            while True:
                try:
                    comp = client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        num_retries=3,
                        **all_kwargs,
                    )
                    break
                except together.error.ServiceUnavailableError:
                    time.sleep(10)
            resp_this = [c.message.content for c in comp.choices]
            assert len(resp_this) == n_this, f'{resp_this = } != {n_this = }'
            resp.extend(resp_this)

        return resp
