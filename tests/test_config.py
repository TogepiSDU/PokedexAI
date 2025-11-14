from app.core.config import settings

# 测试配置是否正确加载
print(f"Doubao API Key: {settings.doubao_api_key}")
print(f"Doubao API Base URL: {settings.doubao_api_base_url}")
print(f"App Host: {settings.app_host}")
print(f"App Port: {settings.app_port}")