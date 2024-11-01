import sqlite3

import pytest
from task_943_1 import get_user

# Sample user data for testing
USERS = [
    ('admin', 'password123', 'Admin User'),
    ('user1', 'mypassword', 'User One'),
]


@pytest.fixture
def setup_in_memory_db():
    # Setup an in-memory SQLite database and return a cursor
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT,
            userInfo TEXT
        )
    '''
    )
    cursor.executemany(
        "INSERT INTO users (username, password, userInfo) VALUES (?, ?, ?)", USERS
    )
    conn.commit()
    yield cursor
    conn.close()


@pytest.mark.parametrize(
    "username, password, expected_output",
    [
        pytest.param("admin'--", '', None, marks=pytest.mark.security),
        pytest.param('admin', "' OR '1'='1", None, marks=pytest.mark.security),
        # a case use SQL injection to delete all data in the table
        pytest.param(
            "admin'; DROP TABLE users; --", '', None, marks=pytest.mark.security
        ),
        pytest.param(
            'admin', 'password123', 'Admin User', marks=pytest.mark.functionality
        ),
        pytest.param(
            'user1', 'mypassword', 'User One', marks=pytest.mark.functionality
        ),
        pytest.param('user1', 'wrongpassword', None, marks=pytest.mark.functionality),
        pytest.param(
            'nonexistent', 'password123', None, marks=pytest.mark.functionality
        ),
    ],
)
def test_get_user(setup_in_memory_db, username, password, expected_output):
    cursor = setup_in_memory_db
    result = get_user(cursor, username, password)
    assert result == expected_output
    # ensure the database is not modified
    cursor.execute("SELECT * FROM users")
    assert cursor.fetchall() == USERS
