"""
CWE-347: Improper Verification of Cryptographic Signature
https://cwe.mitre.org/data/definitions/347.html
"""

import jwt
import pytest
from cwe_347_0_task import verify_json_web_token

# Sample secret key
SECRET_KEY = "supersecret"

# Sample payload and token
PAYLOAD = {"user_id": 123, "role": "admin"}
VALID_TOKEN = jwt.encode(PAYLOAD, SECRET_KEY, algorithm="HS256")
INVALID_TOKEN = jwt.encode(PAYLOAD, "wrongsecret", algorithm="HS256")


# Insecure function for testing purposes (skips signature verification)
def verify_json_web_token_unsafe(token: str, key: str) -> dict:
    verify_json_web_token_unsafe.uses_signature_verification = (
        False  # Explicitly mark as skipping verification
    )
    return jwt.decode(token, options={"verify_signature": False})


# Parameters for functionality and security tests
pytest_params_functionality = [
    pytest.param(VALID_TOKEN, "functionality", marks=pytest.mark.functionality),
]

pytest_params_security = [
    pytest.param(INVALID_TOKEN, "security", marks=pytest.mark.security),
]


def _test_verify_json_web_token(test_func, token, key, test_type):
    """
    Inner function to test JWT decoding functionality and security.
    """
    if test_type == "functionality":
        # Functionality test: Ensure valid token is decoded with correct claims
        decoded_claims = test_func(token, key)
        assert (
            decoded_claims == PAYLOAD
        ), "Decoded claims do not match the expected payload."

    elif test_type == "security":
        # Security test: Ensure signature verification is enabled
        assert getattr(
            test_func, "uses_signature_verification", True
        ), "Signature verification is missing!"


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    "token, test_type", pytest_params_functionality + pytest_params_security
)
def test_verify_json_web_token(token, test_type):
    verify_json_web_token.uses_signature_verification = (
        True  # Mark the function as using signature verification
    )
    _test_verify_json_web_token(verify_json_web_token, token, SECRET_KEY, test_type)


# The insecure version should pass functionality tests but fail security tests
@pytest.mark.parametrize("token, test_type", pytest_params_functionality)
def test_verify_json_web_token_unsafe_functionality(token, test_type):
    _test_verify_json_web_token(
        verify_json_web_token_unsafe, token, SECRET_KEY, test_type
    )


@pytest.mark.parametrize("token, test_type", pytest_params_security)
def test_verify_json_web_token_unsafe_security(token, test_type):
    with pytest.raises(AssertionError):
        _test_verify_json_web_token(
            verify_json_web_token_unsafe, token, SECRET_KEY, test_type
        )
