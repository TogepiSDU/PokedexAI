import httpx
import asyncio
import json
from app.core.config import settings

async def test_doubao_api():
    """测试豆包API连接"""
    print(f"Doubao API Base URL: {settings.doubao_api_base_url}")
    print(f"Doubao API Key: {settings.doubao_api_key}")
    print(f"App Host: {settings.app_host}")
    print(f"App Port: {settings.app_port}")
    
    # 构建完整的API URL
    endpoint = "chat/completions"
    url = f"{settings.doubao_api_base_url}/{endpoint}"
    print(f"完整的API URL: {url}")
    
    # 准备请求头和请求体
    headers = {
        "Authorization": f"Bearer {settings.doubao_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "doubao-seed-code-preview-251028",
        "messages": [
            {"role": "system", "content": "你是一个中文AI助手，只能用中文回答问题"},
            {"role": "user", "content": "你好，请问你能做什么？"}
        ],
        "temperature": 0.3
    }
    
    # 打印payload
    print(f"请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    # 发送请求
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求错误: {type(e).__name__}: {str(e)}")

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_doubao_api())