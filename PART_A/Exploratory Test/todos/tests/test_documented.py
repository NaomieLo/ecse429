import pytest
import requests
import json

API_URL = "http://localhost:4567"


def ensure_system_ready():
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"


def create_todo(title="Default Title", description="Default Description"):
    data = {"title": title, "description": description}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "Failed to create todo"
    return response.json()["id"]


#### TODOS ####


def test_get_todos():
    # Create a new todo for validation
    todo_id = create_todo("Test Todo for GET", "Test description for GET")

    # Perform the GET request
    response = requests.get(API_URL + "/todos")
    assert response.status_code == 200, "GET /todos failed"

    # Verify that the todo we created is in the list
    todos = response.json()["todos"]
    assert any(
        todo["id"] == todo_id for todo in todos
    ), "Newly created todo not found in GET response"

    # Clean up by deleting the todo
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos():
    todo_id = create_todo("Test Todo", "Test description")

    # Verify the todo was created correctly
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"Failed to fetch todo with id {todo_id}"
    todo_data = response.json()["todos"][0]
    assert todo_data["title"] == "Test Todo", "Title does not match expected value"
    assert (
        todo_data["description"] == "Test description"
    ), "Description does not match expected value"

    # Clean up by deleting the todo
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos():
    response = requests.head(API_URL + "/todos")
    assert response.status_code == 200, "HEAD /todos failed"
    # There should be no content in the response for a HEAD request
    assert response.content == b"", "HEAD request returned unexpected content"


#### TODOS/:ID ####


def test_get_todos_id():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"GET /todos/{todo_id} failed"

    # Verify the correct todo data
    todo_data = response.json()["todos"][0]
    assert (
        todo_data["title"] == "Test Todo"
    ), "Fetched todo title does not match expected value"
    assert (
        todo_data["description"] == "Test description"
    ), "Fetched todo description does not match expected value"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos_id():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.head(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"HEAD /todos/{todo_id} failed"
    assert response.content == b"", "HEAD request returned unexpected content"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id():
    todo_id = create_todo("Test Todo", "Test description")

    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = requests.post(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"POST /todos/{todo_id} failed"

    # Verify that the POST actually updated the resource
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert (
        response.status_code == 200
    ), f"Failed to fetch todo with id {todo_id} after POST"
    todo_data = response.json()["todos"][0]
    assert (
        todo_data["title"] == "Updated Title"
    ), "POST request did not update the title correctly"
    assert (
        todo_data["description"] == "Updated description"
    ), "POST request did not update the description correctly"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_put_todos_id():
    todo_id = create_todo("Test Todo", "Test description")

    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = requests.put(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"PUT /todos/{todo_id} failed"

    # Verify the todo was updated correctly
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert (
        response.status_code == 200
    ), f"Failed to fetch updated todo with id {todo_id}"
    todo_data = response.json()["todos"][0]
    assert todo_data["title"] == "Updated Title", "Title was not updated correctly"
    assert (
        todo_data["description"] == "Updated description"
    ), "Description was not updated correctly"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_delete_todos_id():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"

    # Verify the todo was deleted
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 404, f"Deleted todo with id {todo_id} still exists"


#### TODOS/:ID/CATEGORIES ####


def test_get_todos_id_categories():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"GET /todos/{todo_id}/categories failed"

    # Verify response structure is as expected
    categories = response.json()
    assert "categories" in categories, "Expected 'categories' key in response"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id_categories():
    todo_id = create_todo("Test Todo", "Test description")
    category_data = {"title": "Test Category"}

    response_category = requests.post(API_URL + "/categories", json=category_data)
    assert response_category.status_code == 201, "Failed to create category"
    category_id = response_category.json()["id"]

    link_data = {"id": category_id}
    response_link = requests.post(
        API_URL + f"/todos/{todo_id}/categories", json=link_data
    )
    assert response_link.status_code == 201, f"POST /todos/{todo_id}/categories failed"

    # Verify the category is linked to the todo
    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert (
        response.status_code == 200
    ), f"Failed to fetch categories of todo with id {todo_id}"
    categories = response.json()["categories"]
    assert any(
        category["id"] == category_id for category in categories
    ), "Category not linked to todo as expected"

    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/categories/{category_id}")


def test_head_todos_id_categories():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.head(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/categories failed"
    assert response.content == b"", "HEAD request returned unexpected content"

    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TODOS/:ID/CATEGORIES/:ID ####


def test_delete_todos_id_categories_id():
    todo_id = create_todo("Test Todo", "Test description")
    category_data = {"title": "Test Category"}

    response_category = requests.post(API_URL + "/categories", json=category_data)
    assert response_category.status_code == 201, "Failed to create category"
    category_id = response_category.json()["id"]

    requests.post(API_URL + f"/todos/{todo_id}/categories", json={"id": category_id})

    response = requests.delete(API_URL + f"/todos/{todo_id}/categories/{category_id}")
    assert response.status_code in [
        200,
        204,
    ], f"DELETE /todos/{todo_id}/categories/{category_id} failed"

    # Verify the category is no longer linked to the todo
    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert (
        response.status_code == 200
    ), f"Failed to fetch categories of todo with id {todo_id}"
    categories = response.json()["categories"]
    assert not any(
        category["id"] == category_id for category in categories
    ), "Category still linked to todo after deletion"

    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/categories/{category_id}")


#### TODOS/:ID/TASKSOF ####


def test_get_todos_id_taskof():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"GET /todos/{todo_id}/tasksof failed"
    task_data = response.json()

    # Confirming response structure
    assert (
        "projects" in task_data
    ), f"Expected 'projects' key in response, got {task_data.keys()}"

    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id_taskof():
    todo_id = create_todo("Test Todo", "Test description")

    # Create a new task
    task_data = {"title": "New Task2", "description": "Task description"}
    response = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response.status_code == 201, f"POST /todos/{todo_id}/tasksof failed"
    created_task = response.json()

    # Verify the task was created correctly and linked to the todo
    assert "id" in created_task, "No 'id' field in task response"
    task_id = created_task["id"]

    response_check = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert (
        response_check.status_code == 200
    ), f"Failed to fetch tasks of todo with id {todo_id}"
    tasks = response_check.json().get("projects", [])
    assert any(
        task["id"] == task_id for task in tasks
    ), f"Task with id {task_id} not found in todo {todo_id}"

    # Clean up
    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/projects/{task_id}")  # Clean up the created project


def test_head_todos_id_taskof():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.head(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/tasksof failed"

    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TODOS/:ID/TASKSOF/:ID ####


def test_delete_todos_id_tasksof_id():
    todo_id = create_todo("Test Todo", "Test description")

    # Create a new task and link it to the todo
    task_data = {"title": "New Task1", "description": "Task description"}
    response_task = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response_task.status_code == 201, "Failed to create Task"
    task_id = response_task.json()["id"]

    # Verify that the task is linked to the todo
    response_check = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert (
        response_check.status_code == 200
    ), f"Failed to fetch tasks of todo with id {todo_id}"
    tasks = response_check.json().get("projects", [])
    assert any(
        task["id"] == task_id for task in tasks
    ), f"Task with id {task_id} not linked to todo {todo_id} as expected"

    # Delete the task link
    response_delete = requests.delete(API_URL + f"/todos/{todo_id}/tasksof/{task_id}")
    assert response_delete.status_code in [
        200,
        204,
    ], f"DELETE /todos/{todo_id}/tasksof/{task_id} failed"

    # Verify the task link was removed
    response_check_after = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert (
        response_check_after.status_code == 200
    ), f"Failed to fetch tasks of todo with id {todo_id} after deletion"
    tasks_after = response_check_after.json().get("projects", [])
    assert not any(
        task["id"] == task_id for task in tasks_after
    ), f"Task with id {task_id} still linked to todo {todo_id}"

    # Clean up
    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(
        f"{API_URL}/projects/{task_id}"
    )  # Clean up the project as well, since it has a relationship with the todo


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
        test_get_todos_not_found,
        test_head_todos_not_found,
        test_delete_todos_not_found,
        test_delete_todos_id_tasksof_id,
        test_head_todos_id_taskof,
        test_post_todos_id_taskof,
        test_get_todos_id_taskof,
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
