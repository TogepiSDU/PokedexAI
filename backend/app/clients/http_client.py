"""通用异步 HTTP 客户端

封装 GET/POST 请求与错误转译，统一生成 JSON 响应与异常。
"""
import httpx
import json
from typing import Dict, Any, Optional
from fastapi import HTTPException


class HTTPClient:
    """异步 HTTP 客户端封装"""
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送 GET 请求

        返回解析后的 JSON；对常见错误进行 FastAPI HTTPException 转译。
        """
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/{endpoint}"
                response = await client.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail=f"未找到请求的资源: {endpoint}")
                raise HTTPException(status_code=500, detail=f"HTTP 请求失败: {str(e)}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"无法连接到服务器: {str(e)}")
            except ValueError as e:
                raise HTTPException(status_code=500, detail=f"JSON 解析失败: {str(e)}")
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送 POST 请求

        以 JSON 形式提交数据；统一错误处理，保证上层拿到结构化异常。
        """
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/{endpoint}"

                
                response = await client.post(url, json=data, headers=headers, timeout=self.timeout)
                

                
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:

                raise HTTPException(status_code=500, detail=f"HTTP 请求失败: {str(e)}")
            except httpx.RequestError as e:

                raise HTTPException(status_code=503, detail=f"无法连接到服务器: {str(e)}")
            except ValueError as e:

                raise HTTPException(status_code=500, detail=f"JSON 解析失败: {str(e)}")
            except Exception as e:

                raise HTTPException(status_code=500, detail=f"未知错误: {str(e)}")