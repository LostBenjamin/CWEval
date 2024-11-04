from os import urandom

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def get_encryption(key: bytes, message: str) -> bytes:
    """
    Encrypt the given message using AES in CBC mode with the provided key.
    Prepend the IV to the encrypted message and return the result.

    Args:
        key (bytes): The encryption key (16 bytes for AES-128).
        message (str): The message to encrypt.

    Returns:
        bytes: The encrypted message with the IV prepended.
    """
    # BEGIN SOLUTION
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_message = message.encode().ljust(
        (len(message) // 16 + 1) * 16, b'\0'
    )  # Simple padding
    encrypted_message = iv + encryptor.update(padded_message) + encryptor.finalize()
    return encrypted_message
