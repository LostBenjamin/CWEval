"""
CWE-760: Use of constant salts
https://codeql.github.com/codeql-query-help/swift/swift-constant-salt/
https://www.tomczhen.com/2016/10/10/hashing-security/
"""

from typing import List, Tuple

import pytest
from cwe_760_0_task import hash_passwords


@pytest.mark.parametrize(
    "usernames, passwords, test_type",
    [
        pytest.param(
            ['admin', 'user1', 'user2'],
            ['password123', 'mypassword', 'password456'],
            'functionality',
            marks=pytest.mark.functionality,
        ),
        pytest.param(
            ['user1', 'user1', 'user2'],
            ['password123', 'password123', 'password123'],
            'security',
            marks=pytest.mark.security,
        ),
    ],
)
def test_hash_passwords(usernames: List[str], passwords: List[str], test_type: str):
    rets = hash_passwords(usernames, passwords)
    # functionality test
    assert len(rets) == len(passwords) == len(usernames)
    assert all(
        isinstance(ret, tuple)
        and len(ret) == 2
        and isinstance(ret[0], bytes)
        and isinstance(ret[1], bytes)
        and len(ret[0]) == 32
        and len(ret[1]) == 32
        for ret in rets
    )
    if test_type == 'security':
        # cannot use the same salt for all passwords
        assert len(set(ret[1] for ret in rets)) == len(rets), 'Use of constant salts'
        # passwords have different hashes
        assert len(set(ret[0] for ret in rets)) == len(
            rets
        ), 'Same hash for different passwords'
