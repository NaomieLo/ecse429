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

#### PROJECTS PAYLOAD TESTS ####

def test_post_projects_malformed_json():
    # post with invalid json data
    malformed_json = '{"title": "test_title", "description": "test_description"'
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL + "/projects", data=malformed_json, headers=headers)

    # expecting bad request response due to bad data
    assert (
        response.status_code == 400
    ), f"POST /projects with malformed json did not return 400 as expected. got {response.status_code} with response: {response.text}"


def test_post_projects_malformed_xml():
    # post with invalid xml data
    malformed_xml = """<projects>
                         <title>title
                       </projects>"""
    headers = {"Content-Type": "application/xml"}

    response = requests.post(API_URL + "/projects", data=malformed_xml, headers=headers)

    # expecting bad request response due to invalid xml
    assert (
        response.status_code == 400
    ), f"POST /projects with malformed xml did not return 400 as expected. got {response.status_code} with response: {response.text}"


def test_post_projects_invalid_xml():
    # attempt to post invalid xml
    invalid_xml = """<projects>
                       <id>10</id>
                     </projects>"""
    headers = {"Content-Type": "application/xml"}

    response = requests.post(API_URL + "/projects", data=invalid_xml, headers=headers)

    # expecting bad request response due to invalid XML (incorrect structure)
    assert (
        response.status_code == 400
    ), f"POST /projects with invalid XML did not return 400 as expected. got {response.status_code} with response: {response.text}"


def test_post_projects_valid_xml():
    # attempt to post valid xml to the projects endpoint
    valid_xml = """<project>
                     <title>Valid XML Title</title>
                     <description>Valid XML Description</description>
                   </project>"""
    headers = {"Content-Type": "application/xml"}

    response = requests.post(API_URL + "/projects", data=valid_xml, headers=headers)

    # expecting successful response
    assert (
        response.status_code == 201
    ), f"POST /projects with valid xml did not return 201. Got {response.status_code} with response: {response.text}"

    # Cleanup
    project_id = None
    if response.status_code == 201:
        project_data = response.json()
        if "id" in project_data:
            project_id = project_data["id"]

    if project_id:
        response = requests.delete(API_URL + f"/projects/{project_id}")
        assert response.status_code in [200, 204], f"DELETE /projects/{project_id} failed"


#### SUMMARY FUNCTION ####
def test_summary():
    passed_tests = 0
    failed_tests = 0
    test_functions = [
        test_post_projects_malformed_json,
        test_post_projects_malformed_xml,
        test_post_projects_invalid_xml,
        test_post_projects_valid_xml,
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

    # run the tests and shut down after
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
