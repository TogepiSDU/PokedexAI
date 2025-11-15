# 宝可梦图鉴问答系统 - 后端技术文档

## 1. 项目概述

宝可梦图鉴问答系统是一个基于LLM的智能问答服务，能够理解用户关于宝可梦的自然语言问题，通过解析意图、检索宝可梦数据，生成准确的回答。

## 2. 技术栈

- **框架**: FastAPI
- **数据库**: SQLite (使用SQLAlchemy ORM)
- **异步支持**: Python asyncio
- **外部服务集成**: 
  - PokeAPI (宝可梦数据获取)
  - 豆包API (意图解析和回答生成)
- **数据验证**: Pydantic V2
- **配置管理**: Pydantic Settings
- **日志管理**: loguru

## 3. 项目结构

```
backend/
├── .env.example         # 环境变量示例文件
├── main.py              # 应用入口点
├── requirements.txt     # Python依赖
└── app/
    ├── api/             # API路由层
    │   ├── __init__.py
    │   ├── ask_api.py   # 问答接口
    │   └── router.py    # 主路由注册
    ├── clients/         # 外部服务客户端
    │   ├── __init__.py
    │   ├── http_client.py      # HTTP基础客户端
    │   ├── pokeapi_client.py   # PokeAPI客户端
    │   └── doubao_client.py    # 豆包API客户端
    ├── core/            # 核心配置
    │   ├── __init__.py
    │   └── config.py    # 应用配置
    ├── db/              # 数据库相关
    │   ├── __init__.py
    │   ├── base.py      # 数据库基类
    │   ├── models.py    # 数据模型
    │   └── session.py   # 数据库会话管理
    ├── repositories/    # 数据访问层
    ├── schemas/         # 数据传输对象
    │   ├── __init__.py
    │   └── ask_schema.py # 问答相关数据模型
    ├── services/        # 业务逻辑层
    │   ├── __init__.py
    │   ├── dex_qa_service.py    # 图鉴问答服务
    │   ├── intent_parser_service.py # 意图解析服务
    │   └── pokemon_service.py   # 宝可梦数据服务
    └── utils/           # 工具函数
```

## 4. 核心模块说明

### 4.1 配置管理 (core/config.py)

`Config` 类使用 Pydantic Settings 管理应用配置，从环境变量加载配置项。

**主要配置项**:
- 数据库配置 (SQLite数据库路径)
- API配置 (CORS、API前缀等)
- 应用配置 (应用名称、调试模式等)
- 外部API配置 (PokeAPI、豆包API的URL和密钥)

### 4.2 数据库层 (db/)

#### 4.2.1 数据模型 (db/models.py)
- `Pokemon`: 宝可梦数据模型，存储宝可梦基础信息
- `PokemonSpecies`: 宝可梦物种数据模型，存储物种详细信息

#### 4.2.2 会话管理 (db/session.py)
- 数据库引擎创建，配置连接池参数
- SQLAlchemy会话工厂管理
- FastAPI依赖函数 `get_db()` 提供数据库会话

### 4.3 API层 (api/)

#### 4.3.1 主路由 (api/router.py)
- 创建主APIRouter实例
- 注册各子路由

#### 4.3.2 问答接口 (api/ask_api.py)
- 提供 `/ask` POST接口，处理用户自然语言问题
- 接收 `AskRequest` 模型的请求数据
- 返回 `AskResponse` 模型的响应数据
- 使用 `DexQAService` 处理核心业务逻辑

### 4.4 服务层 (services/)

#### 4.4.1 图鉴问答服务 (services/dex_qa_service.py)
- `DexQAService`: 核心业务服务，协调各模块完成问答流程
- 主要流程: 意图解析 → 获取宝可梦数据 → 生成回答

#### 4.4.2 意图解析服务 (services/intent_parser_service.py)
- `IntentParserService`: 调用豆包API解析用户问题意图
- 返回意图解析结果，包含宝可梦名称、意图类型等信息

#### 4.4.3 宝可梦数据服务 (services/pokemon_service.py)
- `PokemonService`: 处理宝可梦数据的获取和缓存逻辑
- 先从数据库查询缓存数据，不存在则调用PokeAPI获取
- 支持获取宝可梦基础信息、物种信息和进化链

### 4.5 客户端层 (clients/)

#### 4.5.1 HTTP基础客户端 (clients/http_client.py)
- `HTTPClient`: 封装异步HTTP请求功能
- 提供GET、POST等HTTP方法的异步实现
- 包含请求重试、错误处理等功能

#### 4.5.2 PokeAPI客户端 (clients/pokeapi_client.py)
- `PokeAPIClient`: 封装PokeAPI的调用
- 提供获取宝可梦数据、物种信息和进化链的方法

#### 4.5.3 豆包客户端 (clients/doubao_client.py)
- `DoubaoClient`: 封装豆包API的调用
- 提供意图解析和回答生成的方法
- 处理与豆包LLM的交互逻辑

### 4.6 数据模型 (schemas/)

#### 4.6.1 问答数据模型 (schemas/ask_schema.py)
- `AskRequest`: 定义用户提问请求的数据结构
- `IntentSchema`: 定义意图解析结果的数据结构
- `AskResponse`: 定义问答接口响应的数据结构

## 5. 系统架构与流程

### 5.1 架构设计

系统采用典型的分层架构设计：

```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   API层       │───>│   服务层      │───>│   客户端层    │───>│   外部服务    │
│   (api/)      │    │   (services/) │    │  (clients/)   │    │  (PokeAPI等)  │
└───────────────┘    └───────────────┘    └───────────────┘    └───────────────┘
        │                   │                     │
        ▼                   ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  数据模型层   │<───│  数据访问层   │<───│    数据库     │
│  (schemas/)   │    │ (repositories/)│    │   (SQLite)   │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 5.2 核心流程

1. **接收请求**: API层接收用户自然语言问题
2. **意图解析**: 服务层调用意图解析服务，识别用户意图和目标宝可梦
3. **数据获取**: 服务层调用宝可梦数据服务，先查数据库缓存，若无则调用PokeAPI
4. **生成回答**: 服务层调用豆包客户端，基于宝可梦数据生成自然语言回答
5. **返回结果**: API层将回答和相关信息封装为响应返回给用户

## 6. 数据流向

- **请求流程**: 客户端 → FastAPI应用 → DexQAService → 各子服务 → 外部API/数据库
- **响应流程**: 外部API/数据库 → 各子服务 → DexQAService → FastAPI应用 → 客户端

## 7. 关键技术点

1. **异步处理**: 使用Python asyncio和aiohttp实现高效的异步请求处理
2. **数据缓存**: 采用SQLite数据库缓存宝可梦数据，减少外部API调用
3. **意图识别**: 利用豆包LLM进行自然语言理解和意图解析
4. **模块化设计**: 清晰的分层架构，便于维护和扩展
5. **数据验证**: 使用Pydantic进行严格的请求和响应数据验证

## 8. 部署与配置

### 8.1 环境变量配置

根据 `.env.example` 创建 `.env` 文件，配置以下环境变量：

```
# 数据库连接
DATABASE_URL="sqlite:///./pokedex.db"

# PokeAPI配置
POKEAPI_BASE_URL="https://pokeapi.co/api/v2"

# 豆包API配置
DOUBAO_API_KEY="your_doubao_api_key"
DOUBAO_API_URL="https://api.doubao.com/v1/chat/completions"

# 应用配置
APP_NAME="PokedexAI"
DEBUG="true"
```

### 8.2 依赖安装

```bash
pip install -r requirements.txt
```

### 8.3 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## 9. API文档

FastAPI自动生成Swagger API文档，可通过以下地址访问：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 10. 健康检查

系统提供健康检查接口：

- `GET /health`: 检查服务健康状态

## 11. 日志管理系统

### 11.1 设计方案
系统采用loguru库实现日志管理功能，loguru是一个功能强大且易于使用的Python日志库，提供了丰富的日志功能和简洁的API。

### 11.2 配置说明
日志系统将在`app/core/__init__.py`中进行配置，主要配置项包括：

- **日志级别**: 支持DEBUG、INFO、WARNING、ERROR、CRITICAL
- **日志格式**: 包含时间戳、日志级别、模块名、行号和日志消息
- **日志输出**: 同时输出到控制台和文件
- **日志轮转**: 按大小和时间进行日志文件轮转

### 11.3 使用示例
```python
from loguru import logger

# 记录不同级别的日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
```

### 11.4 集成计划
日志管理系统将在v1.2版本中实现，主要包括：
1. 添加loguru库依赖
2. 配置日志管理系统
3. 替换现有logging调用为loguru
4. 实现日志文件管理和轮转

## 12. 扩展与优化建议

1. **缓存优化**: 引入Redis等内存缓存，进一步提高数据访问速度
2. **错误处理增强**: 添加更完善的错误处理和重试机制
3. **测试覆盖**: 增加单元测试和集成测试覆盖率
4. **部署自动化**: 配置CI/CD流程，实现自动化部署