import random
import pytest
import requests

from test_projects_documented_capabilities import (
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
)
from test_projects_undocumented_capabilities import (
    test_delete_projects,
    test_patch_projects,
    test_options_projects,
    test_patch_projects_id,
    test_options_projects_id,
    test_put_projects_id_categories,
    test_patch_projects_id_categories,
    test_options_projects_id_categories,
)
from test_projects_unexpected_capabilities import (
    test_post_projects_id_categories_id_generation,
    test_get_projects_incorrect_categories,
    test_get_projects_invalid_id_categories,
    test_post_projects_id_categories_with_different_id_formats,
)

API_URL = "http://localhost:4567"

# Setup function to ensure the system is in the correct state
@pytest.fixture(scope="module")
def setup_system():
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"
    return response

# Test Summary function
def test_summary():
    passed_tests = 0
    failed_tests = 0

    # Gather all test functions from different modules
    test_functions = [
        # Documented Tests
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
        
        # Undocumented Tests
        test_delete_projects,
        test_patch_projects,
        test_options_projects,
        test_patch_projects_id,
        test_options_projects_id,
        test_put_projects_id_categories,
        test_patch_projects_id_categories,
        test_options_projects_id_categories,
        
        # Unexpected Tests
        test_post_projects_id_categories_id_generation,
        test_get_projects_incorrect_categories,
        test_get_projects_invalid_id_categories,
        test_post_projects_id_categories_with_different_id_formats,
    ]

    # Shuffle the list to execute tests in a random order
    random.shuffle(test_functions)

    print("\nRunning Randomized Test Suite:\n")
    for test in test_functions:
        try:
            test()  # Run the test function
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
