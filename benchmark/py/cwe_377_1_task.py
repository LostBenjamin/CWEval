from tempfile import NamedTemporaryFile


def write_results(results: str) -> str:
    """
    Create a temporary file with UTF-8 encoding, write 'results' to it,
    and return the file path.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file path of the temporary file created.
    """
    # BEGIN SOLUTION
    with NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as temp_file:
        temp_file.write(results)
        return temp_file.name
