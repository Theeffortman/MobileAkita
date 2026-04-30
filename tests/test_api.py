from fastapi.testclient import TestClient

from honor_agent.server import TASKS, app


def setup_function() -> None:
    TASKS.clear()


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_get_and_run_task() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "name": "数据分析任务",
            "description": "分析销售数据并生成周报",
            "agents": ["data_analyst"],
            "params": {"data_source": "sales_db", "date_range": "last_week"},
        },
    )

    assert create_response.status_code == 201
    task = create_response.json()["data"]
    assert task["status"] == "created"

    get_response = client.get(f"/api/v1/tasks/{task['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["id"] == task["id"]

    run_response = client.post(f"/api/v1/tasks/{task['id']}/run")
    assert run_response.status_code == 200
    result = run_response.json()["data"]
    assert result["status"] == "completed"
    assert result["task_id"] == task["id"]


def test_list_agents() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/agents")

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == "data_analyst"


def test_analyze_github_repository_without_remote_metadata() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/github/analyze",
        json={"url": "https://github.com/Theeffortman/HonorAgent", "include_remote": False},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["owner"] == "Theeffortman"
    assert data["repo"] == "HonorAgent"
    assert data["health_score"] >= 0
    assert data["suggested_tasks"]


def test_analyze_github_repository_rejects_invalid_url() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/github/analyze",
        json={"url": "https://example.com/not-github", "include_remote": False},
    )

    assert response.status_code == 400
