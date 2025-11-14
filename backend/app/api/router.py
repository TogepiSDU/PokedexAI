from fastapi import APIRouter
from app.api import ask_api

# 创建主路由实例
api_router = APIRouter()

# 注册所有子路由
api_router.include_router(ask_api.router)