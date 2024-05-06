from functools import cache
from covid_backend.storage import BaseStorageClient, get_storage_client
from fastapi.testclient import TestClient
import pytest

from covid_backend.server import app


class MockedStorageClient(BaseStorageClient):
    def __init__(self):
        self.storage = {}

    def get_object(self, container: str, key: str) -> str | None:
        return self.storage.get(container, {}).get(key, None)

    def upload_object(self, container: str, key: str, value: str) -> None:
        if container not in self.storage:
            self.storage[container] = {}
        self.storage[container][key] = value

    def delete_object(self, container: str, key: str) -> None:
        if container in self.storage and key in self.storage[container]:
            del self.storage[container][key]


@cache
def get_mocked_client() -> MockedStorageClient:
    client = MockedStorageClient()
    client.upload_object("covid", "2020", "test")
    return client


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_storage_client] = get_mocked_client
    return TestClient(app)
