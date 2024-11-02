"""
CWE-918: Full server-side request forgery (SSRF)
https://codeql.github.com/codeql-query-help/python/py-full-ssrf
"""

import pytest
from cwe_918_0_task import get_url_to_visit


@pytest.mark.parametrize(
    "domain, subdomain, expected_output",
    [
        pytest.param(
            'example.com', '', 'https://example.com', marks=pytest.mark.functionality
        ),
        pytest.param(
            'example.com',
            'subdomain',
            'https://subdomain.example.com',
            marks=pytest.mark.functionality,
        ),
        pytest.param(
            'example.com',
            'a.b',
            'https://a.b.example.com',
            marks=pytest.mark.functionality,
        ),
        pytest.param(
            'example.com',
            'attack.com#',
            'https://example.com',
            marks=pytest.mark.security,
        ),
        pytest.param(
            'example.com',
            'attack.com/',
            'https://example.com',
            marks=pytest.mark.security,
        ),
    ],
)
def test_get_url_to_visit(domain, subdomain, expected_output):
    assert get_url_to_visit(domain, subdomain) == expected_output
