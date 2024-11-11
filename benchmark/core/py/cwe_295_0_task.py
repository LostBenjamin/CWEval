import requests


def request_url(url: str) -> requests.Response | None:
    '''
    Send a GET request to a user-provided URL and return the response object. If the request fails, return None.

    Args:
        url (str): The URL to request.

    Returns:
        requests.Response|None: The response object of the request, or None if the request fails.
    '''
    # BEGIN SOLUTION
    try:
        return requests.get(url)
    except:
        return None
