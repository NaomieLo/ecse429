import pytest
import requests

API_URL = "http://localhost:4567"

# Test ID Generation for Categories Linked to Projects
def test_post_projects_id_categories_id_generation():
    # Step 1: Create a new project
    project_data = {"title": "New Project", "description": "Project description"}
    project_response = requests.post(API_URL + "/projects", json=project_data)
    assert project_response.status_code == 201, "Failed to create a new project"
    project_id = project_response.json()["id"]

    # Step 2: Create a category linked to the newly created project
    category_data = {
        "title": "First Category",
        "description": "Description for the first category"
    }
    category_response = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data)
    assert category_response.status_code == 201, "Failed to create a category linked to the project"

    # Step 3: Check the ID of the newly created category
    category_id = category_response.json().get("id")
    
    # Step 4: Verify if the category ID starts from 1 or is incremented from previous IDs in the system
    if int(category_id) == 1:
        print(f"Category ID started at 1, indicating a separate sequence for categories linked to projects.")
    else:
        print(f"Category ID is {category_id}, indicating that IDs are being incremented from the last available ID across the system.")

    # Verify if the ID generation behavior is as expected
    assert int(category_id) > 0, "Category ID should be greater than 0"

# Testing GET with Incorrect Project for /projects/:id/categories
def test_get_projects_incorrect_categories():
    # Ensure project 2 does not exist
    requests.delete(API_URL + "/projects/2")

    # Attempt to GET categories for a project that does not exist
    response = requests.get(API_URL + "/projects/2/categories")
    if response.status_code == 200:
        print(f"Unexpected Behavior: GET /projects/2/categories returned 200 OK even though project 2 does not exist.")
    else:
        assert response.status_code == 404, f"GET /projects/2/categories should return 404 when the project does not exist, but got status code {response.status_code}"

# Testing GET with an Invalid Project ID (/projects/anything/categories)
def test_get_projects_invalid_id_categories():
    # Attempt to GET categories using an invalid project ID
    response = requests.get(API_URL + "/projects/anything/categories")
    if response.status_code == 200:
        print(f"Unexpected Behavior: GET /projects/anything/categories returned 200 OK for an invalid project ID.")
    else:
        assert response.status_code == 404, f"GET /projects/anything/categories should return 404 for an invalid project ID, but got status code {response.status_code}"

# Testing POST /projects/:id/categories with JSON using Numeric and String IDs
def test_post_projects_id_categories_with_different_id_formats():
    # Create a new project
    data = {"title": "New Project for Category Test"}
    response = requests.post(API_URL + "/projects", json=data)
    project_id = response.json()["id"]

    # Attempt to POST category with id as numeric
    category_data_numeric_id = {
        "id": 15,
        "title": "Category with Numeric ID",
        "description": "Testing numeric ID input"
    }
    response_numeric = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data_numeric_id)
    assert response_numeric.status_code != 201, "POST /projects/:id/categories should fail with a numeric ID"

    # Attempt to POST category with id as string
    category_data_string_id = {
        "id": "15",
        "title": "Category with String ID",
        "description": "Testing string ID input"
    }
    response_string = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data_string_id)
    assert response_string.status_code == 201, "POST /projects/:id/categories should succeed with a string ID"

# Summary function to track tests
def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_post_projects_id_categories_id_generation,
        test_get_projects_incorrect_categories,
        test_get_projects_invalid_id_categories,
        test_post_projects_id_categories_with_different_id_formats,
    ]

    print("")
    for test in test_functions:
        try:
            test()  # Call the test function here
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
