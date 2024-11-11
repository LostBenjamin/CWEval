import multiprocessing as mp
import os
import subprocess
from typing import Any, Callable, List, Tuple

import numpy as np

BENCHMARK_DIR = 'benchmark'


def get_code_from(
    msg: str,
    only_last: bool = False,
    only_first: bool = False,
    add_new_line: bool = False,
) -> str:
    assert not (
        only_last and only_first
    ), '`only_last` and `only_first` cannot be both True'
    tail = '\n' if add_new_line else ''
    code_blocks: List[str] = []
    msg_lines = msg.splitlines()
    i_line = 0
    while i_line < len(msg_lines):
        line = msg_lines[i_line]
        if line.startswith('```'):
            code_lines = []
            i_line += 1
            while i_line < len(msg_lines):
                line = msg_lines[i_line]
                if line.startswith('```'):
                    break
                code_lines.append(line)
                i_line += 1
            # end while for this code block
            code_blocks.append('\n'.join(code_lines) + tail)
            if only_first:
                return code_blocks[0]
        # end if for this code block
        i_line += 1
    # end while for all code blocks
    if only_last:
        return code_blocks[-1]
    return '\n'.join(code_blocks)


def run_in_subprocess(func: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Run a function in a separate subprocess and return its result.

    Args:
        func: The function to run in the subprocess
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        The return value from the function

    Example:
        def memory_intensive_function(x):
            # This will run in its own memory space
            large_list = [i for i in range(10**6)]
            return x * 2

        result = run_in_subprocess(memory_intensive_function, 5)
    """

    def wrapper(func, return_queue, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return_queue.put(result)
        except Exception as e:
            return_queue.put(e)

    # Create a queue to get the return value
    return_queue = mp.Queue()

    # Create and start the process
    process = mp.Process(
        target=wrapper, args=(func, return_queue) + args, kwargs=kwargs
    )
    process.start()

    # Wait for the process to complete
    process.join()

    # Get the result
    result = return_queue.get()

    # Check if the result is an exception
    if isinstance(result, Exception):
        raise result

    return result


def pass_at_k(n, c, k) -> float:
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def exec_cmd(cmd: List[str], check: bool = True) -> Tuple[int, str, str]:
    assert isinstance(cmd, list)
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    return result.returncode, result.stdout, result.stderr


def exec_cmd_shell(cmd: str, check: bool = True) -> Tuple[int, str, str]:
    assert isinstance(cmd, str)
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=check, shell=True
    )
    return result.returncode, result.stdout, result.stderr


def compile_c(src_path: str, compiled_path: str, check: bool = True) -> None:
    os.makedirs(os.path.dirname(compiled_path), exist_ok=True)
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
    returncode, stdout, stderr = exec_cmd_shell(cmd_str, check)
    if returncode != 0:
        print(f'Error compiling {src_path}:\n{stderr}', flush=True)


def compile_c_list(
    src_path_list: List[str],
    compiled_path_list: List[str],
    check: bool = True,
    num_proc: int = 8,
) -> None:
    assert len(src_path_list) == len(compiled_path_list)
    if num_proc == 1:
        for src_path, compiled_path in zip(src_path_list, compiled_path_list):
            compile_c(src_path, compiled_path, check)
    else:
        with mp.Pool(num_proc) as pool:
            pool.starmap(
                compile_c,
                zip(src_path_list, compiled_path_list, [check] * len(src_path_list)),
            )
