import pytest
import requests
import random
import json

API_URL = "http://localhost:4567"


@pytest.fixture(scope="module")
def save_system_state():
    response = requests.get(API_URL + "/todos")
    assert response.status_code == 200, "Failed to get initial state"
    return response.json()


@pytest.fixture(scope="module")
def setup_system():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "Failed to create initial todo for tests"
    return response.json()


def ensure_system_ready():
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"


def restore_system_state(initial_state):
    current_state = requests.get(API_URL + "/todos").json()
    current_ids = {todo["id"] for todo in current_state["todos"]}
    initial_ids = {todo["id"] for todo in initial_state["todos"]}


#### TODOS ####


def test_get_todos():
    response = requests.get(API_URL + "/todos")
    assert response.status_code == 200, "GET /todos failed"


def test_post_todos():
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "POST /todos failed"
    todo_id = response.json()["id"]


def test_head_todos():
    response = requests.head(API_URL + "/todos")
    assert response.status_code == 200, "HEAD /todos failed"


#### TODOS/:ID ####


def test_get_todos_id():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"GET /todos/{todo_id} failed"


def test_head_todos_id():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.head(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"HEAD /todos/{todo_id} failed"


def test_post_todos_id():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    update_data = {"title": "updated_title", "description": "updated_description"}
    response = requests.post(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"POST /todos/{todo_id} failed"


def test_delete_todos_id():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


#### TODOS/:ID/CATEGORIES ####


def test_get_todos_id_categories():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"GET /todos/{todo_id}/categories failed"


def test_head_todos_id_categories():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.head(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/categories failed"


def test_post_todos_id_categories():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    category_data = {"title": "title", "description": "description"}
    response = requests.post(
        API_URL + f"/todos/{todo_id}/categories", json=category_data
    )
    assert response.status_code == 201, f"POST /todos/{todo_id}/categories failed"


#### TODOS/:ID/CATEGORIES/:ID ####


def test_delete_todos_id_categories_id():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    # create a new category in todo
    category_data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/categories", json=category_data)
    assert response.status_code == 201, "Failed to create category"
    category_id = response.json()["id"]

    response = requests.post(
        API_URL + f"/todos/{todo_id}/categories", json={"id": category_id}
    )
    assert (
        response.status_code == 201
    ), f"Failed to link category {category_id} to todo {todo_id}"


#### TODOS/:ID/TASKSOF ####


def test_get_todos_id_taskof():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"GET /todos/{todo_id}/tasksof failed"


def test_head_todos_id_taskof():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.head(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/tasksof failed"


def test_post_todos_id_taskof():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    task_data = {"title": "test_task", "description": "task_description"}
    response = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response.status_code == 201, f"POST /todos/{todo_id}/tasksof failed"


#### TODOS/:ID/TASKSOF/:ID ####
def test_delete_todos_id_taskof_id():
    # create a new todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.delete(API_URL + f"/todos/{todo_id}/tasksof/1")
    assert response.status_code in [
        200,
        204,
        404,
    ], f"DELETE /todos/{todo_id}/tasksof/1 failed"


# Summary function to keep track of tests
@pytest.mark.usefixtures("save_system_state", "setup_system")
def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_get_todos,
        test_head_todos,
        test_post_todos,
        test_get_todos_id,
        test_head_todos_id,
        test_post_todos_id,
        test_delete_todos_id,
        test_get_todos_id_categories,
        test_head_todos_id_categories,
        test_post_todos_id_categories,
        test_delete_todos_id_categories_id,
        test_get_todos_id_taskof,
        test_head_todos_id_taskof,
        test_post_todos_id_taskof,
        test_delete_todos_id_taskof_id,
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


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
