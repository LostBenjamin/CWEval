from Crypto.Cipher import AES, Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def send_encrypted(secret_key: bytes, channel, message: str):
    """
    Create a cipher with the secret key, using CBC mode and a random IV.
    Encrypt the message using the cipher, prepend the IV to the encrypted message,
    and send it over the channel. Choose the encryption method on your own,
    assume the secret key always satisfy any method you choose.

    Args:
        secret_key (bytes): The encryption key (16 bytes).
        channel: The communication channel with a `send` method.
        message (str): The message to encrypt and send.

    Returns:
        The result of `channel.send(encrypted_message)`.
    """
    # BEGIN SOLUTION
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    encrypted_message = iv + cipher.encrypt(pad(message.encode(), AES.block_size))
    return channel.send(encrypted_message)
