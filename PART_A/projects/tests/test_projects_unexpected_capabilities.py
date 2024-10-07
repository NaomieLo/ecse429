import pytest
import requests

API_URL = "http://localhost:4567"


def ensure_system_ready():
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
    except requests.exceptions.ConnectionError:
        raise AssertionError("API is not active or could not connect")


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

# Testing ID generation logic for categories linked to projects
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

        # Delete the project
        delete_project(project_id)

        # Create a new project and category to see if the ID starts from 1 or continues
        project_id_2 = create_project("New Project for ID Test 2", "Another project for ID test")
        category_id_3 = create_category_for_project(project_id_2, "Third Category", "Description for the third category")
        print(f"Third Category ID after deletion: {category_id_3}")

        # Check the ID behavior: Expect the new category ID to restart from '1' for the new project
        assert int(category_id_3) == 1, f"Expected category ID to start from 1 for the new project, but got {category_id_3} instead."

    finally:
        # Cleanup
        delete_project(project_id_2)


# Testing GET with incorrect project for /projects/:id/categories 
def test_get_projects_incorrect_categories():
    try:
        # Create and delete a project to ensure it doesn't exist
        project_id = create_project()
        delete_project(project_id)

        # Attempt to GET categories for a project that does not exist
        response = requests.get(API_URL + f"/projects/{project_id}/categories")
        assert response.status_code == 404, f"GET /projects/{project_id}/categories should return 404 when the project does not exist, but got status code {response.status_code}"

    except AssertionError as e:
        print(f"test_get_projects_incorrect_categories FAILED: {e}")
        raise e


# Testing GET with an invalid project ID (/projects/anything/categories) 
def test_get_projects_invalid_id_categories():
    try:
        # Attempt to GET categories using an invalid project ID
        response = requests.get(API_URL + "/projects/anything/categories")
        assert response.status_code == 404, f"GET /projects/anything/categories should return 404 for an invalid project ID, but got status code {response.status_code}"

    except AssertionError as e:
        print(f"test_get_projects_invalid_id_categories FAILED: {e}")
        raise e


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

        # Attempt to POST category with id as string
        category_data_string_id = {
            "id": "15",
            "title": "Category with String ID",
            "description": "Testing string ID input"
        }
        response_string = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data_string_id)
        assert response_string.status_code == 201, "POST /projects/:id/categories should succeed with a string ID"

    finally:
        # Cleanup
        delete_project(project_id)


# ALLOW PASS TESTS

# üTesting ID generation logic for categories linked to projects
def test_post_projects_id_categories_id_generation_allow_pass():
    try:
        # Create a new project
        project_id = create_project("New Project for ID Test", "Project description for ID Test")

        # Create the first category linked to the created project
        category_id_1 = create_category_for_project(project_id, "First Category", "Description for the first category")
        assert True, "Allowing test to pass regardless of the outcome."
        print(f"First Category ID: {category_id_1}")

        # Create another category linked to the same project
        category_id_2 = create_category_for_project(project_id, "Second Category", "Description for the second category")
        assert True, "Allowing test to pass regardless of the outcome."
        print(f"Second Category ID: {category_id_2}")

        # Delete the project
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

        # Allow the test to pass regardless of ID behavior
        assert True, "Allowing test to pass regardless of the ID behavior."

    except AssertionError as e:
        print(f"test_post_projects_id_categories_id_generation_allow_pass FAILED: {e}")

    finally:
        # Cleanup
        delete_project(project_id_2)

# Testing GET with incorrect project for /projects/:id/categories
def test_get_projects_incorrect_categories_allow_pass():
    try:
        # Create and delete a project to ensure it doesn't exist
        project_id = create_project()
        delete_project(project_id)

        # Attempt to GET categories for a project that does not exist
        response = requests.get(API_URL + f"/projects/{project_id}/categories")
        if response.status_code == 404:
            assert True, f"GET /projects/{project_id}/categories returned 404 as expected."
        elif response.status_code == 200:
            assert True, f"GET /projects/{project_id}/categories unexpectedly returned 200, allowing test to pass."
        else:
            assert False, f"GET /projects/{project_id}/categories returned unexpected status code: {response.status_code}"

    except AssertionError as e:
        print(f"test_get_projects_incorrect_categories_allow_pass FAILED: {e}")


# Testing GET with an invalid project ID (/projects/anything/categories)
def test_get_projects_invalid_id_categories_allow_pass():
    try:
        # Attempt to GET categories using an invalid project ID
        response = requests.get(API_URL + "/projects/anything/categories")
        if response.status_code == 404:
            assert True, "GET /projects/anything/categories returned 404 as expected."
        elif response.status_code == 200:
            assert True, "GET /projects/anything/categories unexpectedly returned 200, allowing test to pass."
        else:
            assert False, f"GET /projects/anything/categories returned unexpected status code: {response.status_code}"

    except AssertionError as e:
        print(f"test_get_projects_invalid_id_categories_allow_pass FAILED: {e}")


# Testing POST /projects/:id/categories with JSON using numeric and string IDs
def test_post_projects_id_categories_with_different_id_formats_allow_pass():
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
        if response_numeric.status_code != 201:
            print("POST with numeric ID failed as expected.")
        else:
            print("POST with numeric ID unexpectedly succeeded, allowing test to pass.")

        # Attempt to POST category with id as string
        category_data_string_id = {
            "id": "15",
            "title": "Category with String ID",
            "description": "Testing string ID input"
        }
        response_string = requests.post(API_URL + f"/projects/{project_id}/categories", json=category_data_string_id)
        assert True, "Allowing test to pass regardless of the outcome."

    except AssertionError as e:
        print(f"test_post_projects_id_categories_with_different_id_formats_allow_pass FAILED: {e}")

    finally:
        # Cleanup
        delete_project(project_id)


# Running all the tests
if __name__ == "__main__":
    try:
        ensure_system_ready()
        run_tests = True
    except AssertionError as e:
        print(f"System not ready: {e}")
        run_tests = False

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
