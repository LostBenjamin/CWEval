import os
import subprocess
from typing import List, Tuple

import fire
from natsort import natsorted


def exec_cmd(cmd: List[str]) -> str:
    assert isinstance(cmd, list)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.returncode, result.stdout, result.stderr


def exec_cmd_shell(cmd: str) -> str:
    assert isinstance(cmd, str)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
    return result.returncode, result.stdout, result.stderr


def compile_c(src_path: str, compiled_path: str) -> None:
    lib_options = [
        '-lsqlite3',
        '-ljwt',
        # '-lcurl',
        '-lssl',
        '-lcrypto',
        '-larchive',
        '$(xml2-config --cflags --libs)',
    ]
    cmd = ['gcc', src_path, '-o', compiled_path] + lib_options
    cmd_str = ' '.join(cmd)
    exec_cmd_shell(cmd_str)


def compile_all_c(src_dir: str, compiled_dir: str) -> None:
    for file in natsorted(os.listdir(src_dir)):
        if file.endswith('.c'):
            src_path = os.path.join(src_dir, file)
            compiled_path = os.path.join(compiled_dir, os.path.splitext(file)[0])
            compile_c(src_path, compiled_path)


if __name__ == '__main__':
    fire.Fire(compile_all_c)
