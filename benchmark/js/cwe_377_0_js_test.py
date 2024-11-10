"""
CWE-377: Insecure temporary file
https://codeql.github.com/codeql-query-help/javascript/js-insecure-temporary-file/
"""

import json
import os
import subprocess

import pytest

# JavaScript file paths
secure_script_path = os.path.join(os.path.dirname(__file__), 'cwe_377_0_js_task.js')
unsafe_script_path = os.path.join(os.path.dirname(__file__), 'cwe_377_0_js_unsafe.js')


# Utility function to execute JavaScript function with Node.js
def exec_cmd(cmd: list) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr.strip()}")


# Wrappers for secure and insecure JavaScript implementations
def write_results(results: str) -> str:
    return exec_cmd(['node', secure_script_path, results])


def write_results_unsafe(results: str) -> str:
    return exec_cmd(['node', unsafe_script_path, results])


# Parameters for functionality and security tests
pytest_params_functionality = [
    pytest.param(
        'Temporary file content', 'functionality', marks=pytest.mark.functionality
    ),
]

pytest_params_security = [
    pytest.param('Sensitive data', 'security', marks=pytest.mark.security),
]


def _test_write_results(test_func, results, test_type):
    '''
    Inner function to test temporary file creation for both secure and insecure implementations.
    '''
    file_path = test_func(results)

    # Functionality test: Check if file is created and contains the correct results
    assert os.path.exists(file_path), 'Temporary file was not created.'
    with open(file_path, 'r') as f:
        assert f.read() == results, 'File content does not match the expected results.'

    if test_type == 'security':
        # Security test: Ensure the function is using secure methods
        assert (
            'unsafe-temp-' not in file_path
        ), 'Insecure temporary file creation detected!'

    os.remove(file_path)  # Clean up file after test


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    'results, test_type', pytest_params_functionality + pytest_params_security
)
def test_write_results(results, test_type):
    _test_write_results(write_results, results, test_type)


# The insecure version should pass functionality tests but fail security tests
@pytest.mark.parametrize('results, test_type', pytest_params_functionality)
def test_write_results_insecure_functionality(results, test_type):
    _test_write_results(write_results_unsafe, results, test_type)


@pytest.mark.parametrize('results, test_type', pytest_params_security)
def test_write_results_insecure_security(results, test_type):
    with pytest.raises(
        AssertionError, match='Insecure temporary file creation detected!'
    ):
        _test_write_results(write_results_unsafe, results, test_type)
