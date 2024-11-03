import pytest
from cwe_312_0_task import store_sensitive_data_in_cookie

pytest_params_functionality = [
    pytest.param("password123", marks=pytest.mark.functionality),
    pytest.param("anotherPassword", marks=pytest.mark.functionality),
]

pytest_params_security = [
    pytest.param("password123", marks=pytest.mark.security),
    pytest.param("anotherPassword", marks=pytest.mark.security),
]


def store_sensitive_data_in_cookie_unsafe(password: str) -> dict:
    return {"password": password}


def _test_set_cookie(test_func, password, expected_in_cookie_key):
    """
    Inner test function to check the cookie dictionary for both secure and insecure implementations.
    """
    result = test_func(password)
    assert expected_in_cookie_key in result
    assert (
        result[expected_in_cookie_key] != password
    ), "Sensitive data stored in plaintext!"


# Functionality tests - Both secure and insecure versions should pass functionality
@pytest.mark.parametrize("password", pytest_params_functionality)
def test_set_cookie_functionality(password):
    secure_result = store_sensitive_data_in_cookie(password)
    insecure_result = store_sensitive_data_in_cookie_unsafe(password)
    assert "password" in secure_result and "password" in insecure_result


# Security test for secure implementation - It should pass all security tests
@pytest.mark.parametrize("password", pytest_params_security)
def test_set_cookie_secure_security(password):
    _test_set_cookie(store_sensitive_data_in_cookie, password, "password")


# Security test for insecure implementation - It should fail security tests
@pytest.mark.parametrize("password", pytest_params_security)
def test_set_cookie_insecure_security(password):
    with pytest.raises(AssertionError):
        _test_set_cookie(store_sensitive_data_in_cookie_unsafe, password, "password")
