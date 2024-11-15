from typing import Dict, List

import boto3

from cweval.ai import AIAPI


class AWSAIClient(AIAPI):
    def __init__(
        self,
        model_name: str = 'us.meta.llama3-1-8b-instruct-v1:0',
        **kwargs,
    ) -> None:
        self.model_name = model_name
        self.kwargs = kwargs
        self.client = boto3.client(service_name='bedrock-runtime')

    def send_message(
        self,
        messages: List[Dict[str, str]],
        **kwargs,
    ) -> List[str]:
        all_kwargs = self.kwargs.copy()
        all_kwargs.update(kwargs)

        msgs = [
            {
                'role': m['role'],
                'content': [{'text': m['content']}],
            }
            for m in messages
        ]
        config = {}  # conversion
        if 'temperature' in all_kwargs:
            config['temperature'] = all_kwargs['temperature']
        if 'max_completion_tokens' in all_kwargs:
            config['maxTokens'] = all_kwargs['max_completion_tokens']
        if 'top_p' in all_kwargs:
            config['topP'] = all_kwargs['top_p']
        if 'stop' in all_kwargs:
            config['stopSequences'] = all_kwargs['stop']

        resps: List[str] = []
        num_samples = all_kwargs.pop('n', 1)
        for i in range(num_samples):
            resp = self.client.converse(
                modelId=self.model_name,
                messages=msgs,
                inferenceConfig=config,
            )
            # ["output"]["message"]["content"][0]["text"]
            resps.append(
                ''.join([c['text'] for c in resp['output']['message']['content']])
            )
            print(f'{i = }', flush=True)

        return resps
