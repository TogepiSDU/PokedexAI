"""pytest 全局 fixtures

提供 base_url 与 HTTP 客户端，便于用例直接使用。
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import BASE_URL
from request_client import RequestClient

@pytest.fixture(scope="session")
def base_url():
    """服务基础地址（可通过环境变量 BASE_URL 覆盖）"""
    return BASE_URL

@pytest.fixture(scope="session")
def client(base_url):
    """会话级 HTTP 客户端"""
    return RequestClient(base_url)