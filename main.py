import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Pokédex AI 智能图鉴系统",
    description="基于自然语言的宝可梦智能图鉴 API，支持问答交互",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """应用启动事件处理函数"""
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建")


@app.get("/", tags=["健康检查"])
async def root():
    """健康检查接口"""
    return {
        "message": "Pokédex AI 智能图鉴系统正在运行",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    # 运行应用
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True  # 开发环境启用热重载
    )