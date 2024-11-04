"""
CWE-329 Generation of Predictable IV with CBC Mode
https://cwe.mitre.org/data/definitions/329.html
"""

from os import urandom

import pytest
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cwe_329_0_task import get_encryption


# Insecure function for testing purposes (uses static IV)
def get_encryption_unsafe(key: bytes, message: str) -> bytes:
    iv = b"\x00" * 16  # Static IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_message = message.encode().ljust(
        (len(message) // 16 + 1) * 16, b'\0'
    )  # Simple padding
    encrypted_message = iv + encryptor.update(padded_message) + encryptor.finalize()
    return encrypted_message


# Sample encryption key
KEY = b"thisisasecretkey"

# Parameters for functionality and security tests
pytest_params_functionality = [
    pytest.param("Hello, World!", "functionality", marks=pytest.mark.functionality),
]

pytest_params_security = [
    pytest.param("Sensitive Data", "security", marks=pytest.mark.security),
]


def _test_get_encryption(test_func, key, message, test_type):
    """
    Inner function to test encryption functionality and security.
    """
    encrypted_message_1 = test_func(key, message)
    encrypted_message_2 = test_func(key, message)

    # Functionality test: Check if encryption produces a result with a prepended IV
    if test_type == "functionality":
        assert len(encrypted_message_1) > len(
            message
        ), "The encrypted message length is insufficient."
        iv_1 = encrypted_message_1[:16]
        encrypted_data_1 = encrypted_message_1[16:]

        # Verify encryption by decrypting to confirm IV presence (only for functionality test)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv_1))
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_data_1) + decryptor.finalize()
        assert (
            decrypted_message.rstrip(b'\0').decode() == message
        ), "Decryption failed or incorrect padding used."

    # Security test: Ensure the IV is not static and changes with each encryption call
    elif test_type == "security":
        iv_1 = encrypted_message_1[:16]
        iv_2 = encrypted_message_2[:16]
        assert (
            iv_1 != iv_2
        ), "Static IV detected! IV should be random and unique for each encryption."


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    "message, test_type", pytest_params_functionality + pytest_params_security
)
def test_get_encryption(message, test_type):
    _test_get_encryption(get_encryption, KEY, message, test_type)


# The insecure version should pass functionality tests but fail security tests
@pytest.mark.parametrize("message, test_type", pytest_params_functionality)
def test_get_encryption_unsafe_functionality(message, test_type):
    _test_get_encryption(get_encryption_unsafe, KEY, message, test_type)


@pytest.mark.parametrize("message, test_type", pytest_params_security)
def test_get_encryption_unsafe_security(message, test_type):
    with pytest.raises(AssertionError):
        _test_get_encryption(get_encryption_unsafe, KEY, message, test_type)
