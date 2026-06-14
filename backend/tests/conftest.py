"""conftest.py：pytest 公共 fixture。"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """同步测试客户端（用 httpx）。"""
    with TestClient(app) as c:
        yield c
