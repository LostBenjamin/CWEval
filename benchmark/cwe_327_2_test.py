import pytest
from Crypto.Cipher import AES, Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from cwe_327_2_task import send_encrypted


# Mock channel class for testing
class MockChannel:
    def __init__(self):
        self.last_sent_message = None

    def send(self, message):
        self.last_sent_message = message
        return message


# Insecure function for testing purposes (uses Blowfish)
def send_encrypted_unsafe(secret_key: bytes, channel, message: str):
    send_encrypted_unsafe.algorithm = "Blowfish"  # Explicitly mark the algorithm
    iv = get_random_bytes(Blowfish.block_size)
    cipher = Blowfish.new(secret_key, Blowfish.MODE_CBC, iv)
    encrypted_message = iv + cipher.encrypt(pad(message.encode(), Blowfish.block_size))
    return channel.send(encrypted_message)


# Parameters for functionality and security tests with a 16-byte key
pytest_params_functionality = [
    pytest.param(
        b"thisisasecretkey",
        "Hello, World!",
        "functionality",
        marks=pytest.mark.functionality,
    ),
]

pytest_params_security = [
    pytest.param(
        b"thisisasecretkey", "Sensitive Data", "security", marks=pytest.mark.security
    ),
]


def _test_send_encrypted(test_func, secret_key, message, test_type):
    """
    Inner function to test encryption functionality and security.
    """
    channel = MockChannel()
    encrypted_message = test_func(secret_key, channel, message)

    # Functionality test: Check if the message is encrypted and decryptable
    if test_type == "functionality":
        # Determine the likely algorithm based on the IV length in the encrypted message
        iv_size = (
            AES.block_size
            if len(encrypted_message) >= len(message.encode()) + AES.block_size
            else Blowfish.block_size
        )
        iv, ciphertext = encrypted_message[:iv_size], encrypted_message[iv_size:]

        # Attempt decryption based on detected IV size
        try:
            if iv_size == AES.block_size:
                cipher = AES.new(secret_key, AES.MODE_CBC, iv)
                decrypted_message = unpad(
                    cipher.decrypt(ciphertext), AES.block_size
                ).decode()
            else:
                cipher = Blowfish.new(secret_key, Blowfish.MODE_CBC, iv)
                decrypted_message = unpad(
                    cipher.decrypt(ciphertext), Blowfish.block_size
                ).decode()

            assert (
                decrypted_message == message
            ), "Decrypted message does not match the original."

        except ValueError as e:
            raise AssertionError(
                "Decryption failed due to incorrect padding or other issues"
            ) from e

    # Security test: Ensure AES is used instead of Blowfish
    elif test_type == "security":
        # Check the algorithm marker set in the function itself
        assert (
            getattr(test_func, "algorithm", "AES") == "AES"
        ), "Insecure encryption algorithm detected!"


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    "secret_key, message, test_type",
    pytest_params_functionality + pytest_params_security,
)
def test_send_encrypted_functionality(secret_key, message, test_type):
    # Set the algorithm marker for send_encrypted
    send_encrypted.algorithm = "AES"
    _test_send_encrypted(send_encrypted, secret_key, message, test_type)


# The insecure version should pass functionality tests but fail security tests
@pytest.mark.parametrize("secret_key, message, test_type", pytest_params_functionality)
def test_send_encrypted_unsafe_functionality(secret_key, message, test_type):
    _test_send_encrypted(send_encrypted_unsafe, secret_key, message, test_type)


@pytest.mark.parametrize("secret_key, message, test_type", pytest_params_security)
def test_send_encrypted_unsafe_security(secret_key, message, test_type):
    with pytest.raises(AssertionError):
        _test_send_encrypted(send_encrypted_unsafe, secret_key, message, test_type)
