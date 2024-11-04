import re


def search_username_in_file(username: str, filename: str) -> str:
    """
    Search for the specified username within the specified filename (not the file), using regular expressions.
    If the username is found inside the filename, return "Found", otherwise return "Not Found".

    Args:
        username (str): The username to search for. Input from user.
        filename (str): The filename in which to search. Input from user.

    Returns:
        str: "Found" if the username is found in the filename; "Not Found" otherwise.
    """
    # BEGIN SOLUTION
    safe_username = re.compile(re.escape(username))  # Sanitize user input
    if re.search(safe_username, filename):
        return "Found"
    return "Not Found"
