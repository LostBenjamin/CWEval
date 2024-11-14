import abc
import os
from typing import Dict, List


class AIAPI(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        model_name: str,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def send_message(self, messages: List[Dict[str, str]], **kwargs) -> List[str]:
        raise NotImplementedError


def make_aiapi(ai: str, rank: int = 0, **kwargs) -> AIAPI:
    if_name, model_name = ai.split(':')

    if if_name == 'openai':
        from cweval.ai.openai import OpenAIClient

        return OpenAIClient(
            api_key=os.environ['OPENAI_API_KEY'],
            model_name=model_name,
            **kwargs,
        )

    elif if_name.startswith('vllm-openai'):
        # if_name = 'vllm-openai/host/port'
        from cweval.ai.openai import OpenAIClient

        _, host, port = if_name.split('/')
        return OpenAIClient(
            api_key=os.environ['OPENAI_API_KEY'],
            model_name=model_name,
            base_url=f'http://{host}:{port}/v1',
            **kwargs,
        )

    elif if_name == 'google':
        from cweval.ai.google import GoogleAIClient

        return GoogleAIClient(
            api_key=os.environ['GG_API_KEY'],
            model_name=model_name,
            **kwargs,
        )

    elif if_name == 'anvtx':
        from cweval.ai.anvtx import AnVtxClient

        return AnVtxClient(
            model_name=model_name,
            cred_file=os.environ['GC_CRED_FILE'],
            project_id=os.environ['GC_PROJECT_ID'],
            **kwargs,
        )

    elif if_name == 'gcloud':
        from cweval.ai.gcloud import GCloudClient

        return GCloudClient(
            model_name=model_name,
            rank=rank,
            cred_file=os.environ['GC_CRED_FILE'],
            project_id=os.environ['GC_PROJECT_ID'],
            **kwargs,
        )

    else:
        raise Exception(f'Unknown ai interface {if_name}')
