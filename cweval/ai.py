import abc
import subprocess
from typing import Dict, List

CMD = '''docker run -it --rm \
    --pull=always \
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.24-nikolaik \
    -e SANDBOX_USER_ID=$(id -u) \
    -e WORKSPACE_MOUNT_PATH=$WORKSPACE_BASE \
    -e LLM_API_KEY=$LLM_API_KEY \
    -e LLM_MODEL=$LLM_MODEL \
    -e LOG_ALL_EVENTS=true \
    -v $WORKSPACE_BASE:/opt/workspace_base \
    -v ./{}:/task.txt \
    -v ~/.openhands-state:/.openhands-state \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --add-host host.docker.internal:host-gateway \
    --name openhands-myapp-{} \
    docker.all-hands.dev/all-hands-ai/openhands:0.24 \
    python -m openhands.core.main -f /task.txt
'''

CMDO = '''docker run -it --rm \
    --pull=always \
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.24-nikolaik \
    -e SANDBOX_USER_ID=$(id -u) \
    -e WORKSPACE_MOUNT_PATH=$WORKSPACE_BASE \
    -e LLM_API_KEY=$LLM_API_KEY \
    -e LLM_MODEL=$LLM_MODEL \
    -e LLM_MAX_OUTPUT_TOKENS=30000 \
    -e LOG_ALL_EVENTS=true \
    -v $WORKSPACE_BASE:/opt/workspace_base \
    -v ./{}:/task.txt \
    -v ~/.openhands-state:/.openhands-state \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --add-host host.docker.internal:host-gateway \
    --name openhands-myapp-{} \
    docker.all-hands.dev/all-hands-ai/openhands:0.24 \
    python -m openhands.core.main -f /task.txt
'''

CMDO1MINI = '''docker run -it --rm \
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.24-nikolaik \
    -e SANDBOX_USER_ID=$(id -u) \
    -e WORKSPACE_MOUNT_PATH=$WORKSPACE_BASE \
    -e LLM_API_KEY=$LLM_API_KEY \
    -e LLM_MODEL=$LLM_MODEL \
    -e LLM_MAX_OUTPUT_TOKENS=30000 \
    -e LOG_ALL_EVENTS=true \
    -v $WORKSPACE_BASE:/opt/workspace_base \
    -v ./{}:/task.txt \
    -v ~/.openhands-state:/.openhands-state \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --add-host host.docker.internal:host-gateway \
    --name openhands-myapp-{} \
    openhands-o1-mini \
    python -m openhands.core.main -f /task.txt
'''


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

        n_samples = all_kwargs.pop('n', 1)
        max_n_per_req = 1

        rank = self.req_kwargs['rank']
        message = messages[0]['content']
        fname = f'./tmp_{rank}.txt'
        with open(fname, 'w') as f:
            f.write(message)
        if 'o1-mini' in self.model:
            cmd = CMDO1MINI.format(fname, rank)
        elif 'o1' in self.model or 'o3' in self.model:
            cmd = CMDO.format(fname, rank)
        else:
            cmd = CMD.format(fname, rank)

        resp: List[str] = []
        for i, idx in enumerate(range(0, n_samples, max_n_per_req)):
            n_this = min(max_n_per_req, n_samples - i * max_n_per_req)
            if n_this > 1:
                all_kwargs['n'] = n_this
            else:
                all_kwargs.pop('n', 1)

            output = subprocess.check_output(cmd, shell=True)
            resp.append(output.decode('utf-8'))

        return resp
