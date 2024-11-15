import json
from typing import Dict, List

from cweval.ai.aws import AWSAIClient


class AWSIvkAIClient(AWSAIClient):

    def send_message(
        self,
        messages: List[Dict[str, str]],
        **kwargs,
    ) -> List[str]:
        all_kwargs = self.kwargs.copy()
        all_kwargs.update(kwargs)

        req_dict: Dict[str, str] = {}
        assert len(messages) == 1 and messages[0]['role'] == 'user'
        req_dict['prompt'] = messages[0]['content']
        if 'temperature' in all_kwargs:
            req_dict['temperature'] = all_kwargs['temperature']
        if 'max_completion_tokens' in all_kwargs:
            req_dict['max_gen_len'] = all_kwargs['max_completion_tokens']
        if 'top_p' in all_kwargs:
            req_dict['top_p'] = all_kwargs['top_p']

        resps: List[str] = []
        num_samples = all_kwargs.pop('n', 1)
        for i in range(num_samples):
            resp = self.client.invoke_model(
                modelId=self.model_name,
                body=json.dumps(req_dict),
            )
            model_resp = json.loads(resp['body'].read())
            resps.append(model_resp['generation'])

            print(f'{i = }', flush=True)

        return resps
