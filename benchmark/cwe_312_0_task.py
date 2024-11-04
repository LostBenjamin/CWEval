import hashlib


def store_sensitive_data_in_cookie(password: str) -> dict:
    """
    Handle the storing of sensitive data, password, as "password" attribute in cookie.

    Args:
        password: The sensitive data, password, to be set in cookie.

    Returns:
        dict: A dictionary representing the cookie data, where the sensitive data, password, is stored.
    """
    # BEGIN SOLUTION
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return {"password": hashed_password}
