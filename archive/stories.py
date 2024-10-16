import requests

API_URL = "http://localhost:4567"


def create_todo_request(title, done_status, description):
    return requests.post(
        f"{API_URL}/todos",
        json={"title": title, "doneStatus": done_status, "description": description},
    )


def update_todo_request(todo_id, title=None, description=None):
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    return requests.put(f"{API_URL}/todos/{todo_id}", json=data)


def delete_todo_request(todo_id):
    return requests.delete(f"{API_URL}/todos/{todo_id}")


def get_todos_request():
    return requests.get(f"{API_URL}/todos")


def get_categories_for_todo_request(todo_id):
    return requests.get(f"{API_URL}/todos/{todo_id}/categories")


def link_task_to_todo_request(todo_id, task_title, task_description):
    return requests.post(
        f"{API_URL}/todos/{todo_id}/tasksof",
        json={"title": task_title, "description": task_description},
    )
