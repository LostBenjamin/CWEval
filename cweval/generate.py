"""
Expected directory structure:

benchmark
├── core
│   ├── c
│   │   ├── cwe_022_0_c_task.c
│   └── py
│   |   ├── cwe_020_0_task.py
└── lang

evals
├── eval_241110_014704
│   ├── generated_0
│   │   ├── core
│   │   │   ├── c
│   │   │   │   ├── cwe_022_0_c_raw.c    <--- to generate
│   │   │   └── py
│   │   │       ├── cwe_020_0_raw.py
│   │   └── lang
│   └── generated_1
└── pytest.ini
"""

import datetime
import json
import os
import shutil
from typing import Any, Dict, List

import fire
from natsort import natsorted
from p_tqdm import p_map
from tqdm import tqdm

from cweval.ai import make_aiapi
from cweval.commons import BENCHMARK_DIR
from cweval.ppt import make_prompt


class Gener:

    begin_prompt_anchor = 'BEGIN PROMPT'
    begin_solution_anchor = 'BEGIN SOLUTION'

    def __init__(
        self,
        eval_dir: str = '',
        ai: str = 'openai:gpt-4o-mini-2024-07-18',
        ppt: str = 'direct',
        num_proc: int = 8,
        # AI parameters
        n: int = 20,
        max_completion_tokens: int = 2048,
        temperature: float = 1.0,
        **kwargs,
    ):
        self.ai = ai
        self.ppt = ppt
        self.num_proc = num_proc
        self.ai_kwargs = {
            'n': n,
            'max_completion_tokens': max_completion_tokens,
            'temperature': temperature,
            **kwargs,
        }

        if not eval_dir:
            self.eval_dir = os.path.join(
                'evals', f'eval_{datetime.datetime.now().strftime("%y%m%d_%H%M%S")}'
            )
        else:
            self.eval_dir = eval_dir

        self.cases = self._get_cases()

    def _get_cases(self) -> Dict[str, Dict[str, str]]:
        cases: Dict[str, str] = {}
        for root, _, files in os.walk(BENCHMARK_DIR):
            if '__pycache__' in root:
                continue
            for file in natsorted(files):
                file_wo_ext, ext = os.path.splitext(file)
                if not (ext and file_wo_ext.endswith('_task')):
                    continue
                task_file_path = os.path.join(root, file)
                lang = ext[1:]
                with open(task_file_path, 'r') as f:
                    task_code = f.read()
                begin_solution_line_src = ''
                for line in task_code.splitlines():
                    if self.begin_solution_anchor in line:
                        begin_solution_line_src = line
                        break
                if not begin_solution_line_src:
                    raise ValueError(f'No solution found in {task_file_path}')
                code_prompt = (
                    task_code.split(self.begin_prompt_anchor)[-1]
                    .split(begin_solution_line_src)[0]
                    .strip()
                )

                rel_task_file_path = os.path.relpath(task_file_path, BENCHMARK_DIR)
                gen_file_path_template = os.path.join(
                    self.eval_dir,
                    'generated_{index}',
                    rel_task_file_path.replace('_task', '_raw'),
                )

                cases[task_file_path] = {
                    'code_prompt': code_prompt,
                    'lang': lang,
                    'out_path_template': gen_file_path_template,
                }

        return cases

    @staticmethod
    def _gen_case(
        ai: str,
        ppt: str,
        case: Dict[str, str],
        ai_kwargs: Dict[str, Any],
    ) -> None:
        aiapi = make_aiapi(ai, **ai_kwargs)
        prompt = make_prompt(ppt)
        resps = prompt.req_ai(
            aiapi,
            case['lang'],
            case['code_prompt'],
        )
        for i, resp in enumerate(resps):
            out_path = case['out_path_template'].format(index=i)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w') as f:
                f.write(resp)

    def gen(self) -> None:
        p_map(
            self._gen_case,
            [self.ai] * len(self.cases),
            [self.ppt] * len(self.cases),
            self.cases.values(),
            [self.ai_kwargs] * len(self.cases),
            num_cpus=self.num_proc,
        )


if __name__ == "__main__":
    fire.Fire(Gener)
