import pytest
import requests
import json

API_URL = "http://localhost:4567"


def ensure_system_ready():
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"


def test_post_xml_fail():
    data = {"title": "test_title", "description": "test_description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "Failed to create todo"
    todo_id = response.json()["id"]

    invalid_xml = """<todos>
                       <id>10</id>
                     </todos>"""
    headers = {"Content-Type": "application/xml"}
    response = requests.post(
        API_URL + f"/todos/{todo_id}/categories", data=invalid_xml, headers=headers
    )
    assert (
        response.status_code == 400
    ), f"POST /todos/{todo_id}/categories with invalid XML did not return 400"

    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_post_xml_pass():
    data = {"title": "test_title", "description": "test_description"}
    response = requests.post(API_URL + "/todos", json=data)
    assert response.status_code == 201, "Failed to create todo"
    todo_id = response.json()["id"]

    valid_xml = """<category>
                     <title>title</title>
                   </category>"""
    headers = {"Content-Type": "application/xml"}
    response = requests.post(
        API_URL + f"/todos/{todo_id}/categories", data=valid_xml, headers=headers
    )
    assert (
        response.status_code == 200 or response.status_code == 201
    ), f"POST /todos/{todo_id}/categories with valid XML did not return 200 or 201"

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

    response = requests.delete(API_URL + f"/todos/{todo_id}")
    assert response.status_code in [200, 204], f"DELETE /todos/{todo_id} failed"


def test_post_todos_malformed_json():
    malformed_json = '{"title": "test_title", "description": "test_description"'
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL + "/todos", data=malformed_json, headers=headers)

    assert (
        response.status_code == 400
    ), f"POST /todos with malformed JSON did not return 400 as expected. Got {response.status_code} with response: {response.text}"


def test_post_todos_malformed_xml():
    malformed_xml = """<todos>
                         <title>title
                       </todos>"""
    headers = {"Content-Type": "application/xml"}

    response = requests.post(API_URL + "/todos", data=malformed_xml, headers=headers)

    assert (
        response.status_code == 400
    ), f"POST /todos with malformed XML did not return 400 as expected. Got {response.status_code} with response: {response.text}"


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


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
