import pytest
import requests
import json

API_URL = "http://localhost:4567"


def ensure_system_ready():
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
    except requests.exceptions.ConnectionError:
        raise AssertionError("API is not active or could not connect")


def test_post_xml_fail():
    # create todo for testing invalid xml post
    data = {"title": "test_title", "description": "test_description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "failed to create todo"
    todo_id = response.json()["id"]

    # attempt to post invalid xml to the category endpoint
    invalid_xml = """<todos>
                       <id>10</id>
                     </todos>"""
    headers = {"Content-Type": "application/xml"}
    response = requests.post(
        API_URL + f"/todos/{todo_id}/categories", data=invalid_xml, headers=headers
    )
    assert (
        response.status_code == 400
    ), f"POST /todos/{todo_id}/categories with invalid xml did not return 400"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_post_xml_pass():
    # create todo for testing valid xml post
    data = {"title": "test_title", "description": "test_description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "failed to create todo"
    todo_id = response.json()["id"]

    # attempt to post valid xml to category endpoint
    valid_xml = """<category>
                     <title>title</title>
                   </category>"""
    headers = {"Content-Type": "application/xml"}
    response = requests.post(
        API_URL + f"/todos/{todo_id}/categories", data=valid_xml, headers=headers
    )
    assert (
        response.status_code == 200 or response.status_code == 201
    ), f"POST /todos/{todo_id}/categories with valid xml did not return 200 or 201"

    # delete category if created
    category_id = None
    if response.status_code == 201:
        category_data = response.json()
        if "id" in category_data:
            category_id = category_data["id"]

    if category_id:
        response = requests.delete(API_URL + f"/categories/{category_id}")
        assert response.status_code in [
            200,
            204,
        ], f"DELETE /categories/{category_id} failed"

    # cleanup
    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_post_todos_malformed_json():
    # post with malformed json data
    malformed_json = '{"title": "test_title", "description": "test_description"'
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL + "/todos", data=malformed_json, headers=headers)

    # expecting bad request response due to malformed json
    assert (
        response.status_code == 400
    ), f"POST /todos with malformed json did not return 400 as expected. got {response.status_code} with response: {response.text}"


def test_post_todos_malformed_xml():
    # post with malformed xml data
    malformed_xml = """<todos>
                         <title>title
                       </todos>"""
    headers = {"Content-Type": "application/xml"}

    response = requests.post(API_URL + "/todos", data=malformed_xml, headers=headers)

    # expecting bad request response due to malformed xml
    assert (
        response.status_code == 400
    ), f"POST /todos with malformed xml did not return 400 as expected. got {response.status_code} with response: {response.text}"


def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_post_todos_malformed_json,
        test_post_todos_malformed_xml,
        test_post_xml_pass,
        test_post_xml_fail,
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
