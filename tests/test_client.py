import httpx
import pytest

from honor_agent import HonorAgent
from honor_agent.server import TASKS, app


@pytest.fixture(autouse=True)
def clear_tasks() -> None:
    TASKS.clear()


@pytest.mark.asyncio
async def test_sdk_create_and_run_task() -> None:
    transport = httpx.ASGITransport(app=app)
    original_async_client = httpx.AsyncClient

    class LocalAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            kwargs["base_url"] = "http://testserver"
            super().__init__(*args, **kwargs)

    httpx.AsyncClient = LocalAsyncClient  # type: ignore[assignment]
    try:
        client = HonorAgent(api_key="test-key", base_url="http://testserver")
        task = await client.tasks.create(name="Example", agents=["data_analyst"])
        result = await client.tasks.run(task.id)
        insight = await client.github.analyze(
            "https://github.com/Theeffortman/HonorAgent",
            include_remote=False,
        )
    finally:
        httpx.AsyncClient = original_async_client  # type: ignore[assignment]

    assert task.name == "Example"
    assert result.status == "completed"
    assert insight.repo == "HonorAgent"
