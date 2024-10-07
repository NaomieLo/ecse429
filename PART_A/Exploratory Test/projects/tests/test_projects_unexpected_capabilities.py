import pytest
import requests

API_URL = "http://localhost:4567"

# Helper functions for creating and deleting projects
def create_project(title="Default Project", description="Default Description"):
    data = {"title": title, "description": description}
    response = requests.post(API_URL + "/projects", json=data)
    assert response.status_code == 201, "Failed to create project"
    return response.json()["id"]

def delete_project(project_id):
    response = requests.delete(API_URL + f"/projects/{project_id}")
    assert response.status_code in [200, 204], f"DELETE /projects/{project_id} failed"

# Helper function for creating a category for a project
def create_category_for_project(project_id, title="Default Category", description="Default Description"):
    category_data = {"title": title, "description": description}
    response = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data)
    assert response.status_code == 201, "Failed to create category linked to the project"
    return response.json()["id"]

# Testing ID generation logic
def test_post_projects_id_categories_id_generation():
    try:
        # Create a new project
        project_id = create_project("New Project for ID Test", "Project description for ID Test")

        # Create the first category linked to the created project
        category_id_1 = create_category_for_project(project_id, "First Category", "Description for the first category")
        assert int(category_id_1) > 0, "Category ID should be greater than 0"
        print(f"First Category ID: {category_id_1}")

        # Create another category linked to the same project
        category_id_2 = create_category_for_project(project_id, "Second Category", "Description for the second category")
        assert int(category_id_2) > int(category_id_1), "Category IDs should increment"
        print(f"Second Category ID: {category_id_2}")

        # Delete both categories
        delete_project(project_id)

        # Create a new project and category to see if the ID starts from 1 or continues
        project_id_2 = create_project("New Project for ID Test 2", "Another project for ID test")
        category_id_3 = create_category_for_project(project_id_2, "Third Category", "Description for the third category")
        print(f"Third Category ID after deletion: {category_id_3}")

        # Check the ID behavior
        if int(category_id_3) == 1:
            print("Category ID started at 1, indicating a separate sequence for categories linked to each project.")
        else:
            print(f"Category ID is {category_id_3}, indicating that IDs are being incremented from the last available ID across the system.")

        # Cleanup
        delete_project(project_id_2)

    except AssertionError as e:
        print(f"test_post_projects_id_categories_id_generation FAILED: {e}")

# Testing GET with incorrect project for /projects/:id/categories
def test_get_projects_incorrect_categories():
    try:
        # Ensure project 2 does not exist
        requests.delete(API_URL + "/projects/2")

        # Attempt to GET categories for a project that does not exist
        response = requests.get(API_URL + "/projects/2/categories")
        assert response.status_code == 404, f"GET /projects/2/categories should return 404 when the project does not exist, but got status code {response.status_code}"

        print("test_get_projects_incorrect_categories PASSED")

    except AssertionError as e:
        print(f"test_get_projects_incorrect_categories FAILED: {e}")

# Testing GET with an Invalid Project ID (/projects/anything/categories)
def test_get_projects_invalid_id_categories():
    try:
        # Attempt to GET categories using an invalid project ID
        response = requests.get(API_URL + "/projects/anything/categories")
        assert response.status_code == 404, f"GET /projects/anything/categories should return 404 for an invalid project ID, but got status code {response.status_code}"

        print("test_get_projects_invalid_id_categories PASSED")

    except AssertionError as e:
        print(f"test_get_projects_invalid_id_categories FAILED: {e}")

# Testing POST /projects/:id/categories with JSON using numeric and string IDs
def test_post_projects_id_categories_with_different_id_formats():
    try:
        # Create a new project
        project_id = create_project("New Project for Category Test")

        # Attempt to POST category with id as numeric
        category_data_numeric_id = {
            "id": 15,
            "title": "Category with Numeric ID",
            "description": "Testing numeric ID input"
        }
        response_numeric = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data_numeric_id)
        assert response_numeric.status_code != 201, "POST /projects/:id/categories should fail with a numeric ID"
        print("POST with numeric ID failed as expected.")

        # Attempt to POST category with id as string
        category_data_string_id = {
            "id": "15",
            "title": "Category with String ID",
            "description": "Testing string ID input"
        }
        response_string = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data_string_id)
        assert response_string.status_code == 201, "POST /projects/:id/categories should succeed with a string ID"
        print("POST with string ID succeeded as expected.")

        # Cleanup
        delete_project(project_id)

    except AssertionError as e:
        print(f"test_post_projects_id_categories_with_different_id_formats FAILED: {e}")

# Running all the tests
if __name__ == "__main__":
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"

        # Execute all tests
        test_post_projects_id_categories_id_generation()
        test_get_projects_incorrect_categories()
        test_get_projects_invalid_id_categories()
        test_post_projects_id_categories_with_different_id_formats()

    except AssertionError as e:
        print(f"System not ready: {e}")
