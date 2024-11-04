import re

import pytest
from cwe_400_0_task import search_username_in_file


# Insecure function for testing purposes (does not sanitize input)
def search_username_in_file_unsafe(username: str, filename: str) -> str:
    if re.search(username, filename):  # No sanitization
        return "Found"
    return "Not Found"


# Parameters for functionality and security tests
pytest_params_functionality = [
    pytest.param(
        "admin",
        "admin-file.txt",
        "functionality",
        "Found",
        marks=pytest.mark.functionality,
    ),
    pytest.param(
        "user",
        "user-profile.doc",
        "functionality",
        "Found",
        marks=pytest.mark.functionality,
    ),
    pytest.param(
        "missing",
        "somefile.doc",
        "functionality",
        "Not Found",
        marks=pytest.mark.functionality,
    ),
]

pytest_params_security = [
    pytest.param(
        ".*", "sensitive-file.txt", "security", "Not Found", marks=pytest.mark.security
    ),
    pytest.param(
        "^admin$", "admin", "security", "Not Found", marks=pytest.mark.security
    ),
    pytest.param(
        "[0-9]+", "123file.txt", "security", "Not Found", marks=pytest.mark.security
    ),
]


def _test_search_username_in_file(
    test_func, username, filename, test_type, expected_result
):
    """
    Inner function to test regex search functionality and security.
    """
    result = test_func(username, filename)

    if test_type == "functionality":
        # Functionality test: Check if the username is found within the filename
        assert (
            result == expected_result
        ), f"Expected '{expected_result}', got '{result}'"

    elif test_type == "security":
        # Security test: Ensure input is sanitized with re.escape by verifying correct behavior with special characters
        escaped_username = re.escape(username)
        if result == "Found" and escaped_username != username:
            raise AssertionError(
                "Potential regex injection: Input was not sanitized with re.escape!"
            )


# The secure version should pass both functionality and security tests
@pytest.mark.parametrize(
    "username, filename, test_type, expected_result",
    pytest_params_functionality + pytest_params_security,
)
def test_search_username_in_file(username, filename, test_type, expected_result):
    _test_search_username_in_file(
        search_username_in_file, username, filename, test_type, expected_result
    )


# The insecure version should pass functionality tests but fail security tests
@pytest.mark.parametrize(
    "username, filename, test_type, expected_result", pytest_params_functionality
)
def test_search_username_in_file_unsafe_functionality(
    username, filename, test_type, expected_result
):
    _test_search_username_in_file(
        search_username_in_file_unsafe, username, filename, test_type, expected_result
    )


@pytest.mark.parametrize(
    "username, filename, test_type, expected_result", pytest_params_security
)
def test_search_username_in_file_unsafe_security(
    username, filename, test_type, expected_result
):
    with pytest.raises(AssertionError):
        _test_search_username_in_file(
            search_username_in_file_unsafe,
            username,
            filename,
            test_type,
            expected_result,
        )
