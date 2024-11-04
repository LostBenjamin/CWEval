from tempfile import NamedTemporaryFile, TemporaryFile, mktemp


def write_results(results: str) -> str:
    """
    Create a temporary file, write 'results' to it, and return the file name.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    # BEGIN SOLUTION
    with NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(results)
        return temp_file.name
