import random
import pytest

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
)
from test_payloads import (
    test_post_todos_malformed_json,
    test_post_todos_malformed_xml,
    test_post_xml_pass,
    test_post_xml_fail,
)


def test_summary():
    passed_tests = 0
    failed_tests = 0
    # Gather all test functions from different modules
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

    # random.seed(42)  # Set a fixed seed for reproducibility
    random.shuffle(test_functions)

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


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
