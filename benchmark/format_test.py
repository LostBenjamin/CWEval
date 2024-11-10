import os

import pytest
from natsort import natsorted

BENCHMARK_DIR = 'benchmark'
begin_prompt_anchor = 'BEGIN PROMPT'
begin_solution_anchor = 'BEGIN SOLUTION'
begin_entrypoint_anchor = 'BEGIN ENTRYPOINT'


def test_task_format():
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

            # TODO
            if lang == 'js':
                continue

            assert (
                begin_solution_anchor in task_code
            ), f'No {begin_solution_anchor = } found in {task_file_path}'
            if lang != 'py':
                assert (
                    begin_prompt_anchor in task_code
                ), f'No {begin_prompt_anchor = } found in {task_file_path}'
                assert (
                    begin_entrypoint_anchor in task_code
                ), f'No {begin_entrypoint_anchor = } found in {task_file_path}'
