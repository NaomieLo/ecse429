import pytest
import requests

API_URL = "http://localhost:4567"


@pytest.mark.run_first
def test_api_is_active():
    print("Testing if the API is active...")
    response = requests.get(API_URL)
    if response.status_code == 200:
        print("API is active and responded with status code 200.")
    else:
        print(f"API is not active, responded with status code {response.status_code}.")
    assert response.status_code == 200, "API is not active"


@pytest.mark.run_last
def test_shutdown():
    print("Testing if the API can be shut down...")
    response = requests.get(API_URL)
    if response.status_code == 200:
        print("API is confirmed to be running. Proceeding to shutdown.")
    else:
        print(
            f"API is already shutdown, responded with status code {response.status_code}."
        )
        assert False, "API is already shutdown"

    try:
        response = requests.get(API_URL + "/shutdown")
        print("Shutdown request sent to the API.")
    except requests.exceptions.ConnectionError:
        print("Connection error encountered. API is likely shut down successfully.")
        assert True
    else:
        if response.status_code == 200:
            print("API shutdown endpoint responded with status code 200.")
        else:
            print(
                f"Shutdown request responded with status code {response.status_code}."
            )
