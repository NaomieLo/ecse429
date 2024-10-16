import requests
from behave import given, when, then

API_URL = "http://localhost:4567"


@given("the API is responsive")
def step_impl(context):
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"


@given("the database contains several todos")
def step_impl(context):
    # Optionally, ensure that there are todos in the database
    # You could create them here or assume the database has been pre-populated
    pass


@given("the database is empty")
def step_impl(context):
    # Optionally, clear all todos to ensure the database is empty
    requests.delete(f"{API_URL}/todos")


@given("the API is down")
def step_impl(context):
    context.api_url = (
        "http://localhost:1234"  # Change URL to simulate an unreachable API
    )


@given('there is an existing todo with title "{title}" and description "{description}"')
def step_impl(context, title, description):
    data = {"title": title, "description": description}
    response = requests.post(f"{API_URL}/todos", json=data)
    assert response.status_code == 201, f"Failed to create todo with title '{title}'"
    context.todo_id = response.json()["id"]


@given('the todo with id "{todo_id}" is marked as completed')
def step_impl(context, todo_id):
    data = {"doneStatus": "true"}
    response = requests.put(f"{API_URL}/todos/{todo_id}", json=data)
    assert response.status_code in [
        200,
        204,
    ], f"Failed to mark todo with id {todo_id} as completed"


@when("the user retrieves all todos")
def step_impl(context):
    context.response = requests.get(f"{API_URL}/todos")


@when('the user attempts to update a todo with id "{todo_id}" with title "{new_title}"')
def step_impl(context, todo_id, new_title):
    data = {"title": new_title}
    context.response = requests.put(f"{API_URL}/todos/{todo_id}", json=data)


@when(
    'the todo with id "{todo_id}" is updated with title "{new_title}" and description "{new_description}"'
)
def step_impl(context, todo_id, new_title, new_description):
    data = {"title": new_title, "description": new_description}
    context.response = requests.put(f"{API_URL}/todos/{todo_id}", json=data)


@when('the user deletes the todo with id "{todo_id}"')
def step_impl(context, todo_id):
    context.response = requests.delete(f"{API_URL}/todos/{todo_id}")


@when('the user retrieves categories for the todo with id "{todo_id}"')
def step_impl(context, todo_id):
    context.response = requests.get(f"{API_URL}/todos/{todo_id}/categories")


@when(
    'a new task with title "{task_title}" and description "{task_description}" is created for the todo with id "{todo_id}"'
)
def step_impl(context, task_title, task_description, todo_id):
    data = {"title": task_title, "description": task_description}
    context.response = requests.post(f"{API_URL}/todos/{todo_id}/tasksof", json=data)


@then("the status code {status_code:d} will be received")
def step_impl(context, status_code):
    assert (
        context.response.status_code == status_code
    ), f"Expected {status_code}, but got {context.response.status_code}"


@then("the response contains a list of todos")
def step_impl(context):
    todos = context.response.json()
    assert "todos" in todos, "Response does not contain 'todos' key"


@then('the todo with title "{todo_name}" is included in the list')
def step_impl(context, todo_name):
    todos = context.response.json()["todos"]
    assert any(
        todo["title"] == todo_name for todo in todos
    ), f"Todo with title '{todo_name}' not found in response"


@then("the response contains an empty list")
def step_impl(context):
    todos = context.response.json()["todos"]
    assert len(todos) == 0, "Expected an empty list, but found some todos"


@then('the response contains categories "{category1}" and "{category2}"')
def step_impl(context, category1, category2):
    categories = context.response.json()["categories"]
    category_titles = [category["title"] for category in categories]
    assert category1 in category_titles and category2 in category_titles, (
        f"Expected categories '{category1}' and '{category2}' in the response, "
        f"but got {category_titles}"
    )


@then('the response contains the todo with title "{expected_title}"')
def step_impl(context, expected_title):
    response_data = context.response.json()
    assert "title" in response_data, "Title not found in the response"
    assert (
        response_data["title"] == expected_title
    ), f"Expected title '{expected_title}' but got '{response_data['title']}'"


@then("the todo with id {todo_id} should no longer exist in the database")
def step_impl(context, todo_id):
    response = requests.get(f"{API_URL}/todos/{todo_id}")
    assert (
        response.status_code == 404
    ), f"Expected 404 but got {response.status_code}. The todo with id '{todo_id}' still exists."


@then('an error message "{error_message}" will be displayed')
def step_impl(context, error_message):
    assert (
        error_message in context.response.text
    ), f"Expected error message '{error_message}' but got {context.response.text}"
