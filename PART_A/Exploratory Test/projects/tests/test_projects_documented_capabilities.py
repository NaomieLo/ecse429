import pytest
import requests

API_URL = "http://localhost:4567"

# Documented Capabilities Tests

# Setup function to ensure the system is in the correct state
@pytest.fixture(scope="module")
def setup_system():
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"
    return response

### Testing /projects
def test_get_projects():
    response = requests.get(API_URL + "/projects")
    assert response.status_code == 200, "GET /projects failed"

def test_post_projects():
    data = {"title": "New Project", "description": "Project description"}
    response = requests.post(API_URL + "/projects", json=data)
    assert response.status_code == 201, "POST /projects failed"

def test_head_projects():
    response = requests.head(API_URL + "/projects")
    assert response.status_code == 200, "HEAD /projects failed"

### Testing /projects/:id
def test_get_projects_id():
    # Create a new project
    data = {"title": "Project 1", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    response = requests.get(API_URL + f"/projects/{project_id}")
    assert response.status_code == 200, f"GET /projects/{project_id} failed"

def test_put_projects_id():
    # Create a new project
    data = {"title": "Project 2", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Update the project using PUT
    update_data = {"title": "Updated Project 2", "description": "Updated description"}
    response = requests.put(API_URL + f"/projects/{project_id}", json=update_data)
    assert response.status_code in [200, 204], f"PUT /projects/{project_id} failed"

def test_delete_projects_id():
    # Create a new project
    data = {"title": "Project 3", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Delete the project
    response = requests.delete(API_URL + f"/projects/{project_id}")
    assert response.status_code in [200, 204], f"DELETE /projects/{project_id} failed"

### Testing /projects/:id/categories
def test_post_projects_id_categories():
    # Create a new project
    data = {"title": "Project 4", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Add a category to the project
    category_data = {"title": "Category 1", "description": "Category description"}
    response = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data)
    assert response.status_code == 201, f"POST /projects/{project_id}/categories failed"

def test_get_projects_id_categories():
    # Create a new project
    data = {"title": "Project 5", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Get categories related to the project
    response = requests.get(API_URL + f"/projects/{project_id}/categories")
    assert response.status_code == 200, f"GET /projects/{project_id}/categories failed"

### Testing /projects/:id/tasks
def test_post_projects_id_tasks():
    # Create a new project
    data = {"title": "Project 6", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Add a task to the project
    task_data = {"title": "Task 1", "description": "Task description"}
    response = requests.post(API_URL + f"/projects/{project_id}/tasks", json=task_data)
    assert response.status_code == 201, f"POST /projects/{project_id}/tasks failed"

def test_get_projects_id_tasks():
    # Create a new project
    data = {"title": "Project 7", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Get tasks related to the project
    response = requests.get(API_URL + f"/projects/{project_id}/tasks")
    assert response.status_code == 200, f"GET /projects/{project_id}/tasks failed"

### Testing /projects/:id/tasks/:id
def test_delete_projects_id_tasks_id():
    # Create a new project
    data = {"title": "Project 8", "description": "Description"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Create a task for the project
    task_data = {"title": "Task to Delete", "description": "Task description"}
    response = requests.post(API_URL + f"/projects/{project_id}/tasks", json=task_data)
    task_id = response.json()["id"]

    # Delete the task from the project
    response = requests.delete(API_URL + f"/projects/{project_id}/tasks/{task_id}")
    assert response.status_code in [200, 204], f"DELETE /projects/{project_id}/tasks/{task_id} failed"

### Summary Function to Track Tests
@pytest.mark.usefixtures("setup_system")
def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_get_projects,
        test_head_projects,
        test_post_projects,
        test_get_projects_id,
        test_put_projects_id,
        test_delete_projects_id,
        test_post_projects_id_categories,
        test_get_projects_id_categories,
        test_post_projects_id_tasks,
        test_get_projects_id_tasks,
        test_delete_projects_id_tasks_id,
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

# Running all the tests
if __name__ == "__main__":
    pytest.main([__file__, "-s"])
