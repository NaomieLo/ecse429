import pytest
import requests
import json

API_URL = "http://localhost:4567"


def ensure_system_ready():
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
    except requests.exceptions.ConnectionError:
        raise AssertionError("API is not active or could not connect")


def create_todo(title="Default Title", description="Default Description"):
    data = {"title": title, "description": description}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "Failed to create todo"
    return response.json()["id"]


def test_delete_todos():
    response = requests.delete(API_URL + "/todos")
    assert (
        response.status_code == 405
    ), "DELETE /todos failed with unexpected status code"


def test_put_todos():
    data = {"title": "updated_title", "description": "updated_description"}
    response = requests.put(API_URL + "/todos", json=data)
    assert response.status_code == 405, "PUT /todos failed with unexpected status code"


def test_patch_todos():
    data = {"title": "updated_title"}
    response = requests.patch(API_URL + "/todos", json=data)
    assert (
        response.status_code == 405
    ), "PATCH /todos failed with unexpected status code"


def test_options_todos():
    response = requests.options(API_URL + "/todos")
    assert (
        response.status_code == 200
    ), "OPTIONS /todos failed with unexpected status code"
    assert response.content == b"", "OPTIONS /todos returned unexpected content"


def test_patch_todos_id():
    todo_id = create_todo()

    patch_data = {"title": "patched_title"}
    response = requests.patch(API_URL + f"/todos/{todo_id}", json=patch_data)
    assert (
        response.status_code == 405
    ), f"PATCH /todos/{todo_id} failed with unexpected status code"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_options_todos_id():
    todo_id = create_todo()

    response = requests.options(API_URL + f"/todos/{todo_id}")
    assert (
        response.status_code == 200
    ), f"OPTIONS /todos/{todo_id} failed with unexpected status code"
    assert (
        response.content == b""
    ), f"OPTIONS /todos/{todo_id} returned unexpected content"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_put_todos_id_categories():
    todo_id = create_todo()

    update_data = {"title": "updated_category"}
    response = requests.put(API_URL + f"/todos/{todo_id}/categories", json=update_data)
    assert (
        response.status_code == 405
    ), f"PUT /todos/{todo_id}/categories failed with unexpected status code"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_patch_todos_id_categories():
    todo_id = create_todo()

    patch_data = {"title": "patched_category"}
    response = requests.patch(API_URL + f"/todos/{todo_id}/categories", json=patch_data)
    assert (
        response.status_code == 405
    ), f"PATCH /todos/{todo_id}/categories failed with unexpected status code"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_options_todos_id_categories():
    todo_id = create_todo()

    response = requests.options(API_URL + f"/todos/{todo_id}/categories")
    assert (
        response.status_code == 200
    ), f"OPTIONS /todos/{todo_id}/categories failed with unexpected status code"
    assert (
        response.content == b""
    ), f"OPTIONS /todos/{todo_id}/categories returned unexpected content"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_delete_todos,
        test_put_todos,
        test_patch_todos,
        test_options_todos,
        test_patch_todos_id,
        test_options_todos_id,
        test_put_todos_id_categories,
        test_patch_todos_id_categories,
        test_options_todos_id_categories,
    ]

    print("")
    for test in test_functions:
        try:
            test()
            print(f"Test {test.__name__}: PASSED")
            passed_tests += 1
        except AssertionError as e:
            print(f"Test {test.__name__}: FAILED - {e}")
            failed_tests += 1

    print("\nSummary:")
    print(f"Total tests run: {len(test_functions)}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")


# Running all tests
if __name__ == "__main__":

    # check that system is runnig
    try:
        ensure_system_ready()
        run_tests = True
    except AssertionError as e:
        print(f"System not ready: {e}")
        run_tests = False

    # run the tests and shit down after
    if run_tests:
        pytest.main([__file__, "-s"])
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is already shutdown"
        try:
            response = requests.get(API_URL + "/shutdown")
        except requests.exceptions.ConnectionError:
            assert True
    else:
        print("Tests skipped: API is not running or could not be reached.")
