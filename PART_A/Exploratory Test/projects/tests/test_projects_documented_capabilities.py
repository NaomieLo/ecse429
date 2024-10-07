import pytest
import requests

API_URL = "http://localhost:4567"

# Documented Capabilities Tests

def ensure_system_ready():
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
    except requests.exceptions.ConnectionError:
        raise AssertionError("API is not active or could not connect")


def create_project(title="Default Project", description="Default Description"):
    data = {"title": title, "description": description}
    response = requests.post(API_URL + "/projects", json=data)
    assert response.status_code == 201, "Failed to create project"
    return response.json()["id"]


def delete_project(project_id):
    response = requests.delete(API_URL + f"/projects/{project_id}")
    assert response.status_code in [200, 204], f"DELETE /projects/{project_id} failed"


#### PROJECTS ####
def test_get_projects():
    project_id = create_project("Test Project for GET")

    response = requests.get(API_URL + "/projects")
    assert response.status_code == 200, "GET /projects failed"

    # Cleanup
    delete_project(project_id)


def test_post_projects():
    project_id = create_project("Test Project for POST")

    # Verify the project creation
    response = requests.get(API_URL + f"/projects/{project_id}")
    assert response.status_code == 200, f"GET /projects/{project_id} failed"

    # Cleanup
    delete_project(project_id)


def test_head_projects():
    project_id = create_project("Test Project for HEAD")

    response = requests.head(API_URL + "/projects")
    assert response.status_code == 200, "HEAD /projects failed"

    # Cleanup
    delete_project(project_id)


#### PROJECTS/:ID ####

def test_get_projects_id():
    project_id = create_project("Test Project for GET by ID")

    response = requests.get(API_URL + f"/projects/{project_id}")
    assert response.status_code == 200, f"GET /projects/{project_id} failed"

    # Cleanup
    delete_project(project_id)


def test_put_projects_id():
    project_id = create_project("Test Project for PUT")

    update_data = {"title": "Updated Project", "description": "Updated description"}
    response = requests.put(API_URL + f"/projects/{project_id}", json=update_data)
    assert response.status_code in [200, 204], f"PUT /projects/{project_id} failed"

    # Cleanup
    delete_project(project_id)


def test_delete_projects_id():
    project_id = create_project("Test Project for DELETE")

    # Delete the project
    delete_project(project_id)


#### PROJECTS/:ID/CATEGORIES ####

def test_post_projects_id_categories():
    project_id = create_project("Test Project for POST Categories")

    category_data = {"title": "Test Category", "description": "Category description"}
    response = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data)
    assert response.status_code == 201, f"POST /projects/{project_id}/categories failed"

    # Cleanup
    delete_project(project_id)


def test_get_projects_id_categories():
    project_id = create_project("Test Project for GET Categories")

    response = requests.get(API_URL + f"/projects/{project_id}/categories")
    assert response.status_code == 200, f"GET /projects/{project_id}/categories failed"

    # Cleanup
    delete_project(project_id)


#### PROJECTS/:ID/TASKS ####
def test_post_projects_id_tasks():
    project_id = create_project("Test Project for POST Tasks")

    task_data = {"title": "Test Task", "description": "Task description"}
    response = requests.post(API_URL + f"/projects/{project_id}/tasks", json=task_data)
    assert response.status_code == 201, f"POST /projects/{project_id}/tasks failed"

    # Cleanup
    delete_project(project_id)


def test_get_projects_id_tasks():
    project_id = create_project("Test Project for GET Tasks")

    response = requests.get(API_URL + f"/projects/{project_id}/tasks")
    assert response.status_code == 200, f"GET /projects/{project_id}/tasks failed"

    # Cleanup
    delete_project(project_id)


#### PROJECTS/:ID/TASKS/:ID ####

def test_delete_projects_id_tasks_id():
    project_id = create_project("Test Project for DELETE Task")

    # Create a task for the project
    task_data = {"title": "Test Task to Delete", "description": "Task description"}
    response = requests.post(API_URL + f"/projects/{project_id}/tasks", json=task_data)
    assert response.status_code == 201, "Failed to create task"
    task_id = response.json()["id"]

    # Delete the task from the project
    response = requests.delete(API_URL + f"/projects/{project_id}/tasks/{task_id}")
    assert response.status_code in [200, 204], f"DELETE /projects/{project_id}/tasks/{task_id} failed"

    # Cleanup
    delete_project(project_id)


### Summary Function to Track Tests
def test_summary():
    ensure_system_ready()

    test_functions = [
        test_get_projects,
        test_post_projects,
        test_head_projects,
        test_get_projects_id,
        test_put_projects_id,
        test_delete_projects_id,
        test_post_projects_id_categories,
        test_get_projects_id_categories,
        test_post_projects_id_tasks,
        test_get_projects_id_tasks,
        test_delete_projects_id_tasks_id,
    ]

    passed_tests = 0
    failed_tests = 0

    print("\nExecuting tests:\n")
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


# Running all the tests
if __name__ == "__main__":
    try:
        ensure_system_ready()
        run_tests = True
    except AssertionError as e:
        print(f"System not ready: {e}")
        run_tests = False

    if run_tests:
        test_summary()
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
