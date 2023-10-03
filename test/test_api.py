import json

from requests.auth import HTTPBasicAuth

from conftest import example_task_data

headers = {'Accept': 'application/json'}
auth = HTTPBasicAuth('apikey', '1234abcd')
token_pref = 'Bearer '


def test_create_task(client, example_task_data):
    """Test creating a new task."""
    token_response = client.post("/login", data=json.dumps({'password': 'qwerty'}), content_type="application/json")
    assert token_response.status_code == 200
    task = json.loads(token_response.data.decode("utf-8"))
    token = task["token"]
    assert token is not None

    data = example_task_data
    response = client.post("/tasks", data=json.dumps(data), content_type="application/json",
                           headers={'Authorization': token_pref + token})
    assert response.status_code == 201
    task = json.loads(response.data.decode("utf-8"))
    assert task["title"] == "Test Task"
    assert task["status"] == "to_do"


def test_get_tasks(client):
    """Test get tasks"""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = json.loads(response.data.decode("utf-8"))["tasks"]
    assert len(tasks) >= 1


def test_get_task_by_id(client):
    """Test getting a specific task by ID"""
    response = client.post("/tasks", data=json.dumps(example_task_data), content_type="application/json")
    task = json.loads(response.data.decode("utf-8"))

    response = client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    retrieved_task = json.loads(response.data.decode("utf-8"))
    assert retrieved_task["id"] == task["id"]


def test_update_task(client):
    """Test update task by id"""
    response = client.post("/tasks", data=json.dumps(example_task_data), content_type="application/json")
    task = json.loads(response.data.decode("utf-8"))
    updated_data = {"title": "Updated Task", "status": "Completed"}
    response = client.put(f"/tasks/{task['id']}", data=json.dumps(updated_data), content_type="application/json")
    assert response.status_code == 200
    updated_task = json.loads(response.data.decode("utf-8"))
    assert updated_task["title"] == "Updated Task"
    assert updated_task["status"] == "Completed"


def test_delete_task(client):
    """Test delete task by id"""
    response = client.post("/tasks", data=json.dumps(example_task_data), content_type="application/json")
    task = json.loads(response.data.decode("utf-8"))

    response = client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 204
