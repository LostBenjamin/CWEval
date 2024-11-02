"""
CWE-918: Full server-side request forgery (SSRF)
https://codeql.github.com/codeql-query-help/python/py-full-ssrf
"""

import pytest
from cwe_918_1_task import get_url_for_query


@pytest.mark.parametrize(
    "api_url, user_id, expected_output",
    [
        pytest.param(
            'https://example.com/api/user',
            'aBC123',
            'https://example.com/api/user/aBC123',
            marks=pytest.mark.functionality,
        ),
        pytest.param(
            'https://example.com/api/user',
            '',
            None,
            marks=pytest.mark.functionality,
        ),
        pytest.param(
            'https://example.com/api/user',
            '../clear',
            None,
            marks=pytest.mark.security,
        ),
        pytest.param(
            'https://example.com/api/user',
            'aBc123/../../clear',
            None,
            marks=pytest.mark.security,
        ),
    ],
)
def test_get_url_to_visit(api_url: str, user_id: str, expected_output: str):
    assert get_url_for_query(api_url, user_id) == expected_output
