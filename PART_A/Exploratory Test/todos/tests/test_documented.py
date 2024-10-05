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


#### TODOS ####
def test_get_todos():
    # create todo for get validation
    todo_id = create_todo("Test Todo for GET", "Test description for GET")

    # perform get request
    response = requests.get(API_URL + "/todos")
    assert response.status_code == 200, "GET /todos failed"

    # verify that created todo is in the response
    todos = response.json()["todos"]
    assert any(
        todo["id"] == todo_id for todo in todos
    ), "created todo not found in get response"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos():
    # create and post todo
    todo_id = create_todo("Test Todo", "Test description")

    # verify created todo data matches expected values
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"failed to fetch todo with id {todo_id}"
    todo_data = response.json()["todos"][0]
    assert todo_data["title"] == "Test Todo", "title does not match expected value"
    assert (
        todo_data["description"] == "Test description"
    ), "description does not match expected value"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos():
    # perform head request on todos
    response = requests.head(API_URL + "/todos")
    assert response.status_code == 200, "HEAD /todos failed"

    # head requests should have no content
    assert response.content == b"", "HEAD request returned unexpected content"


#### TODOS/:ID ####


def test_get_todos_id():
    # create a todo to fetch by id
    todo_id = create_todo("Test Todo", "Test description")

    # get todo by id
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"GET /todos/{todo_id} failed"

    # verify todo data matches expected values
    todo_data = response.json()["todos"][0]
    assert todo_data["title"] == "Test Todo", "fetched title does not match"
    assert (
        todo_data["description"] == "Test description"
    ), "fetched description does not match"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_head_todos_id():
    # create a todo to perform head request on
    todo_id = create_todo("Test Todo", "Test description")

    # head request for specific todo
    response = requests.head(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 200, f"HEAD /todos/{todo_id} failed"
    assert response.content == b"", "HEAD request returned unexpected content"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id():
    # create a todo for post update
    todo_id = create_todo("Test Todo", "Test description")

    # post update data to existing todo
    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = requests.post(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"POST /todos/{todo_id} failed"

    # verify that post updated the data correctly
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert (
        response.status_code == 200
    ), f"failed to fetch updated todo with id {todo_id}"
    todo_data = response.json()["todos"][0]
    assert todo_data["title"] == "Updated Title", "title was not updated correctly"
    assert (
        todo_data["description"] == "Updated description"
    ), "description was not updated correctly"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_put_todos_id():
    # create a todo to update with put request
    todo_id = create_todo("Test Todo", "Test description")

    # perform put request to update todo
    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = requests.put(API_URL + f"/todos/{todo_id}", json=update_data)
    assert response.status_code in [200, 204], f"PUT /todos/{todo_id} failed"

    # verify that todo was updated correctly
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert (
        response.status_code == 200
    ), f"failed to fetch updated todo with id {todo_id}"
    todo_data = response.json()["todos"][0]
    assert todo_data["title"] == "Updated Title", "title was not updated correctly"
    assert (
        todo_data["description"] == "Updated description"
    ), "description was not updated correctly"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_delete_todos_id():
    # create a todo to delete
    todo_id = create_todo("Test Todo", "Test description")

    # delete the created todo
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"

    # verify that todo no longer exists
    response = requests.get(API_URL + f"/todos/{todo_id}")
    assert response.status_code == 404, f"deleted todo with id {todo_id} still exists"


#### TODOS/:ID/CATEGORIES ####


def test_get_todos_id_categories():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"GET /todos/{todo_id}/categories failed"

    # check expected response structure
    categories = response.json()
    assert "categories" in categories, "Expected 'categories' key in response"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id_categories():
    todo_id = create_todo("Test Todo", "Test description")
    category_data = {"title": "Test Category"}

    # create a new category
    response_category = requests.post(API_URL + "/categories", json=category_data)
    assert response_category.status_code == 201, "Failed to create category"
    category_id = response_category.json()["id"]

    # link the category to the todo
    link_data = {"id": category_id}
    response_link = requests.post(
        API_URL + f"/todos/{todo_id}/categories", json=link_data
    )
    assert response_link.status_code == 201, f"POST /todos/{todo_id}/categories failed"

    # verify the category is linked to the todo
    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert (
        response.status_code == 200
    ), f"Failed to fetch categories of todo with id {todo_id}"
    categories = response.json()["categories"]
    assert any(
        category["id"] == category_id for category in categories
    ), "Category not linked to todo as expected"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/categories/{category_id}")


def test_head_todos_id_categories():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.head(API_URL + f"/todos/{todo_id}/categories")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/categories failed"
    assert response.content == b"", "HEAD request returned unexpected content"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TODOS/:ID/CATEGORIES/:ID ####


def test_delete_todos_id_categories_id():
    todo_id = create_todo("Test Todo", "Test description")
    category_data = {"title": "Test Category"}

    # create category and link it to todo
    response_category = requests.post(API_URL + "/categories", json=category_data)
    assert response_category.status_code == 201, "Failed to create category"
    category_id = response_category.json()["id"]

    requests.post(API_URL + f"/todos/{todo_id}/categories", json={"id": category_id})

    # delete the link between todo and category
    response = requests.delete(API_URL + f"/todos/{todo_id}/categories/{category_id}")
    assert response.status_code in [
        200,
        204,
    ], f"DELETE /todos/{todo_id}/categories/{category_id} failed"

    # verify the category is no longer linked
    response = requests.get(API_URL + f"/todos/{todo_id}/categories")
    assert (
        response.status_code == 200
    ), f"Failed to fetch categories of todo with id {todo_id}"
    categories = response.json()["categories"]
    assert not any(
        category["id"] == category_id for category in categories
    ), "Category still linked to todo after deletion"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/categories/{category_id}")


#### TODOS/:ID/TASKSOF ####


def test_get_todos_id_taskof():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"GET /todos/{todo_id}/tasksof failed"
    task_data = response.json()

    # confirm response contains 'projects' key
    assert (
        "projects" in task_data
    ), f"Expected 'projects' key in response, got {task_data.keys()}"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


def test_post_todos_id_taskof():
    todo_id = create_todo("Test Todo", "Test description")

    # create a new task and link to todo
    task_data = {"title": "New Task2", "description": "Task description"}
    response = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response.status_code == 201, f"POST /todos/{todo_id}/tasksof failed"
    created_task = response.json()

    # verify the task is linked properly
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

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/projects/{task_id}")


def test_head_todos_id_taskof():
    todo_id = create_todo("Test Todo", "Test description")

    response = requests.head(API_URL + f"/todos/{todo_id}/tasksof")
    assert response.status_code == 200, f"HEAD /todos/{todo_id}/tasksof failed"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")


#### TODOS/:ID/TASKSOF/:ID ####


def test_delete_todos_id_tasksof_id():
    todo_id = create_todo("Test Todo", "Test description")

    # create task and link to todo
    task_data = {"title": "New Task1", "description": "Task description"}
    response_task = requests.post(API_URL + f"/todos/{todo_id}/tasksof", json=task_data)
    assert response_task.status_code == 201, "Failed to create Task"
    task_id = response_task.json()["id"]

    # verify task is linked to todo
    response_check = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert (
        response_check.status_code == 200
    ), f"Failed to fetch tasks of todo with id {todo_id}"
    tasks = response_check.json().get("projects", [])
    assert any(
        task["id"] == task_id for task in tasks
    ), f"Task with id {task_id} not linked to todo {todo_id} as expected"

    # delete the link between task and todo
    response_delete = requests.delete(API_URL + f"/todos/{todo_id}/tasksof/{task_id}")
    assert response_delete.status_code in [
        200,
        204,
    ], f"DELETE /todos/{todo_id}/tasksof/{task_id} failed"

    # verify task link removed
    response_check_after = requests.get(API_URL + f"/todos/{todo_id}/tasksof")
    assert (
        response_check_after.status_code == 200
    ), f"Failed to fetch tasks of todo with id {todo_id} after deletion"
    tasks_after = response_check_after.json().get("projects", [])
    assert not any(
        task["id"] == task_id for task in tasks_after
    ), f"Task with id {task_id} still linked to todo {todo_id}"

    # cleanup
    requests.delete(f"{API_URL}/todos/{todo_id}")
    requests.delete(f"{API_URL}/projects/{task_id}")


#### TEST INSTABILITIES ####


# validate GET request for nonexistent todo returns 404
def test_get_todos_not_found():
    response = requests.get(API_URL + "/todos/10000")
    assert (
        response.status_code == 404
    ), "GET /todos/10000 did not return 404 as expected"


# validate HEAD request for nonexistent todo returns 404
def test_head_todos_not_found():
    response = requests.head(API_URL + "/todos/10000")
    assert (
        response.status_code == 404
    ), "HEAD /todos/10000 did not return 404 as expected"


# validate DELETE request for nonexistent todo returns 404
def test_delete_todos_not_found():
    response = requests.delete(API_URL + "/todos/10000")
    assert (
        response.status_code == 404
    ), "DELETE /todos/10000 did not return 404 as expected"


# test summary that ensures all tests are run and results are displayed
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
