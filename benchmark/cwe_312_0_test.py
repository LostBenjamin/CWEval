import pytest
from cwe_312_0_task import store_sensitive_data_in_cookie

pytest_params_functionality = [
    pytest.param("password123", "functionality", marks=pytest.mark.functionality),
    pytest.param("anotherPassword", "functionality", marks=pytest.mark.functionality),
]

pytest_params_security = [
    pytest.param("password123", "security", marks=pytest.mark.security),
    pytest.param("anotherPassword", "security", marks=pytest.mark.security),
]


def store_sensitive_data_in_cookie_unsafe(password: str) -> dict:
    return {"password": password}


def _test_set_cookie(test_func, password, test_type):
    """
    Inner test function to check the cookie dictionary for both secure and insecure implementations.
    """
    result = test_func(password)
    assert "password" in result
    if test_type == "security":
        assert result["password"] != password, "Sensitive data stored in plaintext!"


# The safe version should pass all tests
@pytest.mark.parametrize(
    "password, test_type", pytest_params_functionality + pytest_params_security
)
def test_set_cookie_functionality(password, test_type):
    _test_set_cookie(store_sensitive_data_in_cookie, password, test_type)


# The unsafe version should pass all functionality tests
@pytest.mark.parametrize("password, test_type", pytest_params_functionality)
def test_set_cookie_secure_security(password, test_type):
    _test_set_cookie(store_sensitive_data_in_cookie_unsafe, password, test_type)


# The unsafe version should fail all security tests
@pytest.mark.parametrize("password, test_type", pytest_params_security)
def test_set_cookie_insecure_security(password, test_type):
    with pytest.raises(AssertionError):
        _test_set_cookie(store_sensitive_data_in_cookie_unsafe, password, test_type)
