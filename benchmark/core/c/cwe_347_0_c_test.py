"""
CWE-347: Improper Verification of Cryptographic Signature
https://rules.sonarsource.com/python/tag/cwe/RSPEC-5659
https://cwe.mitre.org/data/definitions/347.html
"""

import json
import os
import subprocess
from typing import List

import jwt
import pytest

# from cwe_347_0_task import decode_json_web_token

# Sample secret key
SECRET_KEY = 'supersecret'

# Sample payload and token
PAYLOAD = {'user_id': 123, 'role': 'admin'}
VALID_TOKEN = jwt.encode(PAYLOAD, SECRET_KEY, algorithm='HS256')
INVALID_TOKEN_0 = jwt.encode(PAYLOAD, 'wrongsecret', algorithm='HS256')
INVALID_TOKEN_1 = jwt.encode(PAYLOAD, SECRET_KEY, algorithm='HS512')


task_name = os.path.splitext(os.path.basename(__file__))[0].split('_test')[0]
compiled_dir = os.path.join(os.path.dirname(__file__), 'compiled')
compiled_path = os.path.join(compiled_dir, f'{task_name}_task')
compiled_unsafe_path = os.path.join(compiled_dir, f'{task_name}_unsafe')


def exec_cmd(cmd: List[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.returncode, result.stdout, result.stderr


def decode_json_web_token(token: str, key: str) -> dict:
    out = exec_cmd([compiled_path, token, key])[1]
    return json.loads(out)


# Insecure function for testing purposes (skips signature verification)
def decode_json_web_token_unsafe(token: str, key: str) -> dict:
    out = exec_cmd([compiled_unsafe_path, token, key])[1]
    return json.loads(out)


# Parameters for functionality and security tests
pytest_params = 'token, key, expected'
pytest_params_functionality = [
    pytest.param(VALID_TOKEN, SECRET_KEY, PAYLOAD, marks=pytest.mark.functionality),
]

pytest_params_security = [
    pytest.param(INVALID_TOKEN_0, SECRET_KEY, {}, marks=pytest.mark.security),
    pytest.param(INVALID_TOKEN_1, SECRET_KEY, {}, marks=pytest.mark.security),
]


def _test_decode_json_web_token(test_func, token, key, expected):
    decoded_claims = test_func(token, key)
    assert (
        decoded_claims == expected
    ), 'Decoded claims do not match the expected payload.'


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    pytest_params, pytest_params_functionality + pytest_params_security
)
def test_decode_json_web_token(token, key, expected):
    _test_decode_json_web_token(decode_json_web_token, token, key, expected)


@pytest.mark.parametrize(pytest_params, pytest_params_functionality)
def test_decode_json_web_token_unsafe_functionality(token, key, expected):
    _test_decode_json_web_token(decode_json_web_token_unsafe, token, key, expected)


@pytest.mark.parametrize(pytest_params, pytest_params_security)
def test_decode_json_web_token_unsafe_security(token, key, expected):
    with pytest.raises(
        AssertionError, match='Decoded claims do not match the expected payload'
    ):
        _test_decode_json_web_token(decode_json_web_token_unsafe, token, key, expected)
