import pytest
import requests

API_URL = "http://localhost:4567/todos"

# Test cases to validate API functionality.


# GET Requests
def test_get_all_todos():
    print("Test 1.01: GET /todos, output the entries in the todo list")
    response = requests.get(API_URL)
    assert response.status_code == 200
    print(response.json())


def test_get_todo_1():
    print("Test 1.02: GET /todos/1, output entry 1 in the todo list")
    response = requests.get(f"{API_URL}/1")
    assert response.status_code == 200
    print(response.json())


def test_get_todo_3_not_found():
    print("Test 1.03: GET /todos/3, output an error message as expected")
    response = requests.get(f"{API_URL}/3")
    assert response.status_code == 404
    print("Error: Entry not found")


def test_get_todo_hello_not_found():
    print("Test 1.04: GET /todos/hello, output an error message as expected")
    response = requests.get(f"{API_URL}/hello")
    assert response.status_code == 404
    print("Error: Invalid ID format")


def test_get_todos_trailing_slash():
    print("Test 1.05: GET /todos/, expecting 404 not found error")
    response = requests.get(f"{API_URL}/")
    assert response.status_code == 404
    print("Error: 404 not found")


def test_get_todo_title_404():
    print("Test 1.06: GET /todos/1/title, expecting 404 not found error")
    response = requests.get(f"{API_URL}/1/title")
    assert response.status_code == 404
    print("Error: 404 not found")


def test_get_todo_projects():
    print("Test 1.07: GET /todos/1/projects, output the related projects")
    response = requests.get(f"{API_URL}/1/projects")
    assert response.status_code == 200
    print(response.json())


# POST Requests
def test_post_todo_1():
    print("Test 1.08: POST /todos/1, output elements of element with ID 1")
    response = requests.post(f"{API_URL}/1")
    assert response.status_code == 200
    print(response.json())


def test_post_todo_3_not_found():
    print("Test 1.09: POST /todos/3, expecting an error message")
    response = requests.post(f"{API_URL}/3")
    assert response.status_code == 404
    print("Error: Entry not found")


def test_post_todo_with_query():
    print("Test 1.10: POST /todos/1?id=2, output contents of element with ID 1")
    response = requests.post(f"{API_URL}/1?id=2")
    assert response.status_code == 200
    print(response.json())


def test_post_todo_invalid_query():
    print("Test 1.11: POST /todos/1?id=helloworld, expect type error")
    response = requests.post(f"{API_URL}/1?id=helloworld")
    assert response.status_code == 400
    print("Error: Invalid ID type")


# DELETE Requests
def test_delete_todo_1():
    print("Test 1.12: DELETE /todos/1, deleting element with ID 1")
    response = requests.delete(f"{API_URL}/1")
    assert response.status_code == 200
    print("Deleted successfully")


def test_get_deleted_todo():
    print("Test 1.13: GET /todos/1, expecting Not Found")
    response = requests.get(f"{API_URL}/1")
    assert response.status_code == 404
    print("Error: Not Found")


def test_delete_todo_100_not_found():
    print("Test 1.14: DELETE /todos/100, expecting Not Found")
    response = requests.delete(f"{API_URL}/100")
    assert response.status_code == 404
    print("Error: Not Found")


# HEAD Requests
def test_head_todo_2():
    print("Test 1.15: HEAD /todos/2, expecting no error")
    response = requests.head(f"{API_URL}/2")
    assert response.status_code == 200
    print("HEAD request successful for ID 2")


def test_head_todo_1_not_found():
    print("Test 1.16: HEAD /todos/1, expecting Not Found")
    response = requests.head(f"{API_URL}/1")
    assert response.status_code == 404
    print("Error: Not Found since ID 1 was deleted")


# OPTIONS Requests
def test_options_todo_2():
    print("Test 1.17: OPTIONS /todos/2, expecting no error")
    response = requests.options(f"{API_URL}/2")
    assert response.status_code == 200
    print("OPTIONS request successful for ID 2")


def test_options_todo_1():
    print("Test 1.18: OPTIONS /todos/1, expecting Not Found as entry DNE")
    response = requests.options(f"{API_URL}/1")
    assert response.status_code == 404
    print("Error: Not Found since ID 1 was deleted")
