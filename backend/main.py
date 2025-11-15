"""FastAPI 应用入口

- 注册 API 路由与中间件
- 提供健康检查与内部配置诊断接口
- 启动事件中初始化数据库表

本文件仅包含应用装配与通用端点，不包含业务逻辑。
"""
import uvicorn
import sys
import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings
from app.core.exception_handler import register_exception_handlers
from datetime import datetime, timezone

# 设置系统默认编码为 UTF-8（仅在直接运行时生效，避免影响测试捕获）

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Pokédex AI 智能图鉴系统",
    description="基于自然语言的宝可梦智能图鉴 API，支持问答交互",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 设置 API 响应编码：仅对以 /api/ 开头的接口设置 JSON UTF-8 头，避免影响 Swagger 静态资源
@app.middleware("http")
async def add_encoding_header(request, call_next):
    response = await call_next(request)
    # 只对API路由设置JSON编码头，避免干扰Swagger UI
    if request.url.path.startswith("/api/"):
        response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

# 配置 CORS：开发阶段允许所有来源；生产环境建议限定具体域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由，所有业务接口统一挂载到 /api/v1 前缀下
app.include_router(api_router, prefix="/api/v1")

# 注册异常处理器
register_exception_handlers(app)


@app.on_event("startup")
async def startup_event():
    """应用启动事件处理函数

    - 创建/更新数据库表结构
    - 可在此处添加连接池预热、缓存预加载等初始化逻辑
    """
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建")


@app.get("/", tags=["健康检查"])
async def root():
    """健康检查接口

    返回基础运行信息与文档入口，不做权限校验。
    """
    return {
        "message": "Pokédex AI 智能图鉴系统正在运行",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["健康检查"])
async def health():
    """简化健康检查

    仅返回服务状态与时间戳，可用于负载均衡或监控探针。
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/internal/config/doubao")
async def internal_doubao_config():
    """内部诊断端点：检查豆包密钥加载状态

    仅返回布尔值状态，不泄露任何敏感数据。
    """
    from os import getenv
    from pathlib import Path
    file_has_key = False
    try:
        for p in [Path(__file__).resolve().parents[0].parent / ".env", Path(__file__).resolve().parents[1] / ".env"]:
            if p.exists():
                for line in p.read_text(encoding="utf-8").splitlines():
                    if line.startswith("DOUBAO_API_KEY="):
                        v = line.split("=",1)[1].strip()
                        file_has_key = bool(v)
                        if file_has_key:
                            break
            if file_has_key:
                break
    except Exception:
        pass
    return {
        "env": bool(getenv("DOUBAO_API_KEY")),
        "settings": bool(settings.doubao_api_key),
        "file": file_has_key
    }


if __name__ == "__main__":
    # 运行应用
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True  # 开发环境启用热重载
    )