import pytest
import requests
import random
import json

API_URL = "http://localhost:4567"


def ensure_system_ready():
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"


#### TODOS ####


def test_get_todos():
    response = requests.get(API_URL + "/todos")
    assert response.status_code == 200, "GET /todos failed"


def test_post_todos():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "POST /todos failed"
    todo_id = response.json()["id"]

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos():
    response = requests.head(API_URL + "/todos")
    assert response.status_code == 200, "HEAD /todos failed"


#### TODOS/:ID ####


def test_get_todos_id():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"GET /todos/{todo_id} failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos_id():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.head(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"HEAD /todos/{todo_id} failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    update_data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"POST /todos/{todo_id} failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_put_todos_id():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    update_data = {"title": "title", "description": "description"}
    response = requests.put(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"PUT /todos/{todo_id} failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_delete_todos_id():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


#### TODOS/:ID/CATEGORIES ####


def test_get_todos_id_categories():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"GET /todos/{todo_id}/categories failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id_categories():
    todo_data = {"title": "title", "description": "description"}
    category_data = {"title": "title", "description": "description"}

    response_todo = requests.post(API_URL + "/todos", json=todo_data)
    todo_id = response_todo.json()["id"]

    response_category = requests.post(API_URL + "/categories", json=category_data)
    category_id = response_category.json()["id"]

    link_data = {"id": category_id}
    response_link = requests.post(
        API_URL + f"/todos/{todo_id}/categories", json=link_data
    )
    assert response_link.status_code == 201, f"POST /todos/{todo_id}/categories failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/categories/{category_id}")


def test_head_todos_id_categories():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.head(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/categories failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TODOS/:ID/CATEGORIES/:ID ####


def test_delete_todos_id_categories_id():
    todo_data = {"title": "title", "description": "description"}
    category_data = {"title": "title", "description": "description"}

    response_todo = requests.post(API_URL + "/todos", json=todo_data)
    todo_id = response_todo.json()["id"]

    response_category = requests.post(API_URL + "/categories", json=category_data)
    category_id = response_category.json()["id"]

    requests.post(API_URL + f"/todos/{todo_id}/categories", json={"id": category_id})

    response = requests.delete(API_URL + f"/todos/{todo_id}/categories/{category_id}")
    assert response.status_code in [
        200,
        204,
    ], f"DELETE /todos/{todo_id}/categories/{category_id} failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/categories/{category_id}")


#### TODOS/:ID/TASKSOF ####


def test_get_todos_id_taskof():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"GET /todos/{todo_id}/tasksof failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id_taskof():
    # create a ne todo
    data = {"title": " title", "description": " description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    task_data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response.status_code == 201, f"POST /todos/{todo_id}/tasksof failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos_id_taskof():
    data = {"title": "title", "description": "description"}
    response = requests.post(API_URL + "/todos", json=data)
    todo_id = response.json()["id"]

    response = requests.head(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/tasksof failed"

    requests.delete(f"{API_URL}/todos/{todo_id}/tasksof")
    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TODOS/:ID/TASKSOF/:ID ####


def test_delete_todos_id_tasksof_id():

    data = {"title": "title", "description": "description"}
    response_todo = requests.post(API_URL + "/todos", json=data)
    assert response_todo.status_code == 201, "Failed to create Todo"
    todo_id = response_todo.json()["id"]

    task_data = {
        "title": "title",
        "description": "dscription",
        "completed": False,
        "active": False,
    }
    response_task = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response_task.status_code == 201, "Failed to create Task"
    task_id = response_task.json()["id"]

    response_link = requests.post(
        API_URL + f"/todos/{todo_id}/tasksof", json={"id": task_id}
    )
    assert (
        response_link.status_code == 201
    ), f"Failed to link Task {task_id} to Todo {todo_id}"

    response_delete = requests.delete(API_URL + f"/todos/{todo_id}/tasksof/{task_id}")
    assert response_delete.status_code in [
        200,
        204,
    ], f"DELETE /todos/{todo_id}/tasksof/{task_id} failed"

    requests.delete(f"{API_URL}/taskof/{task_id}")
    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TEST INSTABILITIES ####


def test_get_todos_not_found():
    response = requests.get(API_URL + "/todos/10000")
    assert (
        response.status_code == 404
    ), "GET /todos/10000 did not return 404 as expected"


def test_head_todos_not_found():
    response = requests.head(API_URL + "/todos/10000")
    assert (
        response.status_code == 404
    ), "HEAD /todos/10000 did not return 404 as expected"


def test_delete_todos_not_found():
    response = requests.delete(API_URL + "/todos/10000")
    assert (
        response.status_code == 404
    ), "DELETE /todos/10000 did not return 404 as expected"


def test_summary():

    ensure_system_ready()

    test_functions = [
        test_get_todos,
        test_post_todos,
        test_head_todos,
        test_get_todos_id,
        test_head_todos_id,
        test_post_todos_id,
        test_put_todos_id,
        test_delete_todos_id,
        test_get_todos_id_categories,
        test_post_todos_id_categories,
        test_head_todos_id_categories,
        test_delete_todos_id_categories_id,
        test_get_todos_id_taskof,
        test_post_todos_id_taskof,
        test_head_todos_id_taskof,
        test_delete_todos_id_tasksof_id,
        test_get_todos_not_found,
        test_head_todos_not_found,
        test_delete_todos_not_found,
    ]

    passed_tests = 0
    failed_tests = 0

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
