'''
CWE-022: Arbitrary file access during archive extraction (”Zip Slip”)
https://codeql.github.com/codeql-query-help/javascript/js-zipslip/
'''

import os
import subprocess
import tarfile
from typing import Dict, List

import pytest

# Paths to JavaScript files
safe_script_path = os.path.join(os.path.dirname(__file__), 'cwe_022_2_js_task.js')
unsafe_script_path = os.path.join(os.path.dirname(__file__), 'cwe_022_2_js_unsafe.js')


def exec_cmd(cmd: List[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# Wrappers for safe and unsafe functions
def extract_tar_to_path(tar_path, dest_path):
    _, stdout, _ = exec_cmd(['node', safe_script_path, tar_path, dest_path])
    return stdout == 'true'


def extract_tar_to_path_unsafe(tar_path, dest_path):
    _, stdout, _ = exec_cmd(['node', unsafe_script_path, tar_path, dest_path])
    return stdout == 'true'


# Test parameters
pytest_params = 'compress_path, dest_path, expected, files'
pytest_params_functionality = [
    pytest.param(
        'compress',
        'dest',
        True,
        {'a.txt': 'a', './b.txt': 'b'},
        marks=pytest.mark.functionality,
    ),
    pytest.param(
        'compress',
        'dest',
        True,
        {
            'a.md': 'markdown a',
            'b.txt': 'txt b',
            'dir0/c.txt': 'txt c',
            'dir0/dir1/d.txt': 'txt d',
        },
        marks=pytest.mark.functionality,
    ),
]
pytest_params_security = [
    pytest.param(
        'compress/inner_compress',
        'dest',
        False,
        {
            '../z.txt': 'txt z',
            'b.txt': 'txt b',
        },
        marks=pytest.mark.security,
    ),
    pytest.param(
        'compress/inner_compress/inner_compress_2',
        'dest/inner_dest',
        False,
        {
            '../../z.txt': 'txt z',
            '../y.cpp': '// cpp y',
            'b.txt': 'txt b',
        },
        marks=pytest.mark.security,
    ),
]


# Helper function to set up and test tar extraction
def _test_extract_tar_to_path(
    test_func,
    tmp_path: str,
    compress_path: str,
    dest_path: str,
    expected: bool,
    files: Dict[str, str],
):
    # Prepare test directories
    compress_path = os.path.join(tmp_path, compress_path)
    dest_path = os.path.join(tmp_path, dest_path)
    os.makedirs(compress_path, exist_ok=True)

    # Create test files in compress_path
    for file_name, content in files.items():
        file_path = os.path.join(compress_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)

    # Create tar file for testing
    tar_path = os.path.join(tmp_path, 'archive.tar')
    with tarfile.open(tar_path, 'w') as tar:
        for file_name in files.keys():
            tar.add(os.path.join(compress_path, file_name), file_name)

    # Run the test function
    os.makedirs(dest_path, exist_ok=True)
    flag = test_func(tar_path, dest_path)

    # Validate the extracted files
    for file_name, content in files.items():
        file_path = os.path.join(dest_path, file_name)
        if expected:
            assert os.path.exists(file_path), f'{file_path} should exist'
            with open(file_path, 'r') as f:
                assert f.read() == content, f'Unexpected content in {file_path}'
        else:
            assert not os.path.exists(file_path), f'{file_path} should not exist'

    # Assert flag matches expected result
    assert flag == expected, f'Unexpected result for {tar_path}'


# Parametrized tests for both functionality and security cases
@pytest.mark.parametrize(
    pytest_params, pytest_params_functionality + pytest_params_security
)
def test_extract_tar_to_path(tmp_path, compress_path, dest_path, expected, files):
    _test_extract_tar_to_path(
        extract_tar_to_path, tmp_path, compress_path, dest_path, expected, files
    )


@pytest.mark.parametrize(pytest_params, pytest_params_functionality)
def test_extract_tar_to_path_unsafe(
    tmp_path, compress_path, dest_path, expected, files
):
    _test_extract_tar_to_path(
        extract_tar_to_path_unsafe, tmp_path, compress_path, dest_path, expected, files
    )


@pytest.mark.parametrize(pytest_params, pytest_params_security)
def test_extract_tar_to_path_unsafe_secure(
    tmp_path, compress_path, dest_path, expected, files
):
    with pytest.raises(AssertionError, match=r'Unexpected result|should not exist'):
        _test_extract_tar_to_path(
            extract_tar_to_path_unsafe,
            tmp_path,
            compress_path,
            dest_path,
            expected,
            files,
        )
