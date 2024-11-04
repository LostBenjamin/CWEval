import jwt


def verify_json_web_token(token: str, key: str) -> dict:
    """
    Decode the JSON Web Token (JWT) with the provided key and return its claims.

    Args:
        token (str): The JWT token to decode.
        key (str): The secret key used for decoding.

    Returns:
        dict: The decoded claims of the JWT.
    """
    # BEGIN SOLUTION
    decoded_token = jwt.decode(token, key, algorithms=["HS256"])
    return decoded_token
