import hashlib

import pytest
from argon2 import PasswordHasher
from cwe_327_1_task import get_password_hash


# Insecure function for testing purposes (uses SHA-256)
def get_password_hash_unsafe(password: str) -> str:
    get_password_hash_unsafe.uses_argon2 = (
        False  # Explicitly mark this function as using SHA-256
    )
    return hashlib.sha256(password.encode()).hexdigest()


# Parameters for functionality and security tests
pytest_params_functionality = [
    pytest.param("secure_password", marks=pytest.mark.functionality),
]

pytest_params_security = [
    pytest.param("sensitive_password", marks=pytest.mark.security),
]


def _test_get_password_hash(test_func, password, test_type):
    """
    Inner function to test password hashing functionality and security.
    """
    hashed_password = test_func(password)

    # Functionality test: Check if the hashed password can be verified
    if test_type == "functionality":
        if getattr(
            test_func, "uses_argon2", True
        ):  # Verify with Argon2 if the function uses Argon2
            ph = PasswordHasher()
            try:
                assert ph.verify(
                    hashed_password, password
                ), "Password verification failed."
            except Exception as e:
                raise AssertionError("Password verification error") from e
        else:
            # For SHA-256, verify by directly comparing the expected SHA-256 hash
            expected_hash = hashlib.sha256(password.encode()).hexdigest()
            assert (
                hashed_password == expected_hash
            ), "SHA-256 hash mismatch for insecure function."

    # Security test: Ensure Argon2 is used instead of SHA-256
    elif test_type == "security":
        assert getattr(
            test_func, "uses_argon2", False
        ), "Insecure hashing algorithm detected!"


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    "password", pytest_params_functionality + pytest_params_security
)
def test_get_password_hash(password, test_type="functionality"):
    # Mark the function explicitly to use Argon2
    get_password_hash.uses_argon2 = True
    _test_get_password_hash(get_password_hash, password, test_type)


# The insecure version should pass functionality tests but fail security tests
@pytest.mark.parametrize("password", pytest_params_functionality)
def test_get_password_hash_unsafe_functionality(password):
    _test_get_password_hash(get_password_hash_unsafe, password, "functionality")


@pytest.mark.parametrize("password", pytest_params_security)
def test_get_password_hash_unsafe_security(password):
    with pytest.raises(AssertionError):
        _test_get_password_hash(get_password_hash_unsafe, password, "security")
