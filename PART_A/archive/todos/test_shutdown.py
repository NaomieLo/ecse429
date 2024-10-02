import pytest
import requests

API_URL = "http://localhost:4567"


@pytest.mark.run_first
def test_api_is_active():
    print("Testing if the API is active...")
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"


@pytest.mark.run_last
def test_shutdown():
    print("Testing if the API can be shut down...")
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is already shutdown"
    try:
        response = requests.get(API_URL + "/shutdown")
    except requests.exceptions.ConnectionError:
        assert True
