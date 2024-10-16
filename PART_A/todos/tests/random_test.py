import random
import pytest
import requests

# importing tests from different modules
from test_documented import (
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
)
from test_undocumented import (
    test_delete_todos,
    test_put_todos,
    test_patch_todos,
    test_options_todos,
    test_patch_todos_id,
    test_options_todos_id,
    test_put_todos_id_categories,
    test_patch_todos_id_categories,
    test_options_todos_id_categories,
    test_delete_todos_id_categories,
)
from test_payloads import (
    test_post_todos_malformed_json,
    test_post_todos_malformed_xml,
    test_post_xml_pass,
    test_post_xml_fail,
)

from test_unexpected import (
    test_post_todos_id_categories_id_generation,
    test_get_todos_incorrect_categories,
    test_get_todos_invalid_id_categories,
    test_post_todos_id_categories_with_different_id_formats,
    test_get_todos_incorrect_categories_allow_pass,
    test_get_todos_invalid_id_categories_allow_pass,
    test_post_todos_id_categories_with_string_id_allow_pass,
    test_post_todos_id_categories_with_string_id_allow_pass,
)

API_URL = "http://localhost:4567"


def ensure_system_ready():
    # check if api is up and running
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
    except requests.exceptions.ConnectionError:
        raise AssertionError("API is not active or could not connect")


# test summary that ensures all tests are run and results are displayed
def test_summary():
    passed_tests = 0
    failed_tests = 0
    # gather all test functions from different modules
    test_functions = [
        test_post_todos_malformed_json,
        test_post_todos_malformed_xml,
        test_post_xml_pass,
        test_post_xml_fail,
        test_delete_todos,
        test_put_todos,
        test_patch_todos,
        test_options_todos,
        test_patch_todos_id,
        test_options_todos_id,
        test_put_todos_id_categories,
        test_patch_todos_id_categories,
        test_options_todos_id_categories,
        test_get_todos,
        test_post_todos,
        test_head_todos,
        test_get_todos_id,
        test_head_todos_id,
        test_post_todos_id,
        test_put_todos_id,
        test_delete_todos,
        test_put_todos,
        test_patch_todos,
        test_options_todos,
        test_patch_todos_id,
        test_options_todos_id,
        test_put_todos_id_categories,
        test_patch_todos_id_categories,
        test_options_todos_id_categories,
        test_delete_todos_id_categories,
        test_head_todos_id_taskof,
        test_post_todos_id_taskof,
        test_get_todos_id_taskof,
        test_post_todos_id_categories_id_generation,
        test_get_todos_incorrect_categories,
        test_get_todos_invalid_id_categories,
        test_post_todos_id_categories_with_different_id_formats,
        test_get_todos_incorrect_categories_allow_pass,
        test_get_todos_invalid_id_categories_allow_pass,
        test_post_todos_id_categories_with_string_id_allow_pass,
        test_post_todos_id_categories_with_string_id_allow_pass,
    ]

    # shuffle tests for random execution order
    random.shuffle(test_functions)

    print("")
    # run each test and track pass/fail counts
    for test in test_functions:
        try:
            test()
            print(f"Test {test.__name__}: PASSED")
            passed_tests += 1
        except AssertionError as e:
            print(f"Test {test.__name__}: FAILED - {e}")
            failed_tests += 1

    # summary of test results
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
