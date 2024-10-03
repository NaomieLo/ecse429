import pytest
import requests

API_URL = "http://localhost:4567"

# Undocumented Capabilities Tests

### Testing Unsupported HTTP Methods for /projects
def test_delete_projects():
    response = requests.delete(API_URL + "/projects")
    assert response.status_code == 405, "DELETE /projects should not be allowed"

def test_patch_projects():
    data = {"title": "Patch Project"}
    response = requests.patch(API_URL + "/projects", json=data)
    assert response.status_code == 405, "PATCH /projects should not be allowed"

def test_options_projects():
    response = requests.options(API_URL + "/projects")
    assert response.status_code == 200, "OPTIONS /projects failed"

### Testing Unsupported HTTP Methods for /projects/:id
def test_patch_projects_id():
    # Create a new project
    data = {"title": "Patch Project"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Attempt to PATCH the project
    update_data = {"title": "Patched Project"}
    response = requests.patch(API_URL + f"/projects/{project_id}", json=update_data)
    assert response.status_code == 405, f"PATCH /projects/{project_id} should not be allowed"

def test_options_projects_id():
    # Create a new project
    data = {"title": "Options Project"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    response = requests.options(API_URL + f"/projects/{project_id}")
    assert response.status_code == 200, f"OPTIONS /projects/{project_id} failed"

### Testing Unsupported HTTP Methods for /projects/:id/categories
def test_put_projects_id_categories():
    # Attempt to PUT a category to a project, which is not allowed
    response = requests.put(API_URL + "/projects/1/categories")
    assert response.status_code == 405, "PUT /projects/1/categories should not be allowed"

def test_patch_projects_id_categories():
    # Attempt to PATCH a category to a project, which is not allowed
    response = requests.patch(API_URL + "/projects/1/categories")
    assert response.status_code == 405, "PATCH /projects/1/categories should not be allowed"

def test_options_projects_id_categories():
    response = requests.options(API_URL + "/projects/1/categories")
    assert response.status_code == 200, "OPTIONS /projects/1/categories failed"

# Summary function to track tests
def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_delete_projects,
        test_patch_projects,
        test_options_projects,
        test_patch_projects_id,
        test_options_projects_id,
        test_put_projects_id_categories,
        test_patch_projects_id_categories,
        test_options_projects_id_categories,
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
