"""测试配置

读取服务基础地址 BASE_URL，缺省为本机 8000 端口。
"""
import os
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")