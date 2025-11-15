"""轻量 HTTP 客户端（用于测试）

封装 GET/POST，统一超时与 URL 拼接，便于在用例中直接调用。
"""
import requests

class RequestClient:
    def __init__(self, base_url: str, timeout: int = 30):
        """初始化客户端

        Args:
            base_url: 服务基础地址，如 http://127.0.0.1:8000
            timeout: 请求超时（秒）
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, **kwargs):
        """GET 请求

        Args:
            path: 以 / 开头的相对路径
        """
        url = f"{self.base_url}{path}"
        return requests.get(url, timeout=self.timeout, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        """POST 请求（JSON）

        Args:
            path: 以 / 开头的相对路径
            json: JSON 请求体
        """
        url = f"{self.base_url}{path}"
        return requests.post(url, json=json, timeout=self.timeout, **kwargs)