# Pokédex AI 智能图鉴系统 - 项目结构

## 项目概览
Pokédex AI 是一个基于AI的宝可梦图鉴系统，结合了宝可梦数据查询和智能问答功能。

## 技术栈
- **框架**: FastAPI
- **语言**: Python 3.9+
- **数据库**: MySQL
- **外部API**: PokeAPI (宝可梦数据), 豆包API (AI问答)
- **配置管理**: Pydantic Settings
- **HTTP客户端**: httpx

## 目录结构

```
PokedexAI/
├── .env                    # 环境变量配置文件
├── .env.example            # 环境变量示例文件
├── .gitignore              # Git忽略文件
├── README.md               # 项目说明文档
├── main.py                 # 项目入口文件
├── requirements.txt        # 项目依赖
├── app/                    # 主应用代码目录
├── docs/                   # 文档目录
└── tests/                  # 测试目录
    ├── __init__.py
    ├── api/               # API路由层
    │   ├── __init__.py
    │   ├── ask_api.py     # 问答API接口
    │   └── router.py      # 路由注册
    ├── clients/           # 外部API客户端
    │   ├── __init__.py
    │   ├── doubao_client.py  # 豆包API客户端
    │   ├── http_client.py    # HTTP客户端基类
    │   └── pokeapi_client.py # PokeAPI客户端
    ├── core/              # 核心配置
    │   ├── __init__.py
    │   └── config.py      # 系统配置
    ├── db/                # 数据库相关
    │   ├── __init__.py
    │   ├── base.py        # 数据库基础类
    │   ├── models.py      # 数据库模型
    │   └── session.py     # 数据库会话
    ├── repositories/      # 数据访问层
    │   ├── __init__.py
    │   └── pokemon_repository.py # 宝可梦数据仓库
    ├── schemas/           # 数据模型定义
    │   ├── __init__.py
    │   └── ask_schema.py  # 问答相关数据模型
    ├── services/          # 业务逻辑层
    │   ├── __init__.py
    │   ├── dex_qa_service.py       # 图鉴问答服务
    │   ├── intent_parser_service.py # 意图解析服务
    │   └── pokemon_service.py      # 宝可梦数据服务
    └── utils/             # 工具类
        └── __init__.py
```

## 模块说明

### 1. 根目录文件
- **.env**: 存储项目的环境变量，包括数据库连接信息、API密钥等
- **.env.example**: 环境变量示例文件，展示需要配置的变量名
- **.gitignore**: Git版本控制的忽略文件配置
- **main.py**: 项目的入口文件，启动FastAPI应用
- **requirements.txt**: 列出项目所需的Python依赖包
- **README.md**: 项目的主要说明文档

### 2. docs/ - 文档目录
- **PROJECT_STRUCTURE.md**: 项目结构文档
- **《Pokédex AI 智能图鉴系统》技术方案设计文档（TDD）.md**: 技术方案设计文档
- **《Pokédex AI 智能图鉴系统》需求文档（PRD）.md**: 需求文档

### 3. tests/ - 测试目录
- **test_api.py**: API测试脚本
- **test_config.py**: 配置测试脚本
- **test_doubao_config.py**: 豆包API配置测试脚本
- **test_token_consumption.py**: 令牌消耗测试脚本

### 4. app/api/ - API路由层
- **router.py**: 注册所有API路由
- **ask_api.py**: 实现问答相关的API接口，处理用户的宝可梦相关问题

### 5. app/clients/ - 外部API客户端
- **http_client.py**: 封装HTTP请求的基础客户端类
- **pokeapi_client.py**: 与PokeAPI交互的客户端，获取宝可梦数据
- **doubao_client.py**: 与豆包API交互的客户端，实现AI问答功能

### 6. app/core/ - 核心配置
- **config.py**: 使用Pydantic Settings管理项目配置，从环境变量中读取配置信息

### 7. app/db/ - 数据库相关
- **base.py**: 数据库基础类，定义ORM基类
- **models.py**: 定义数据库表结构的模型类
- **session.py**: 管理数据库会话，提供数据库连接

### 8. app/repositories/ - 数据访问层
- **pokemon_repository.py**: 封装宝可梦数据的数据库操作

### 9. app/schemas/ - 数据模型定义
- **ask_schema.py**: 定义问答相关的请求和响应数据模型

### 10. app/services/ - 业务逻辑层
- **pokemon_service.py**: 处理宝可梦数据的业务逻辑
- **intent_parser_service.py**: 解析用户意图，识别用户的问题类型
- **dex_qa_service.py**: 整合宝可梦数据和AI问答功能，提供完整的图鉴问答服务

## 核心流程

1. 用户通过API接口发送宝可梦相关问题
2. API路由层接收请求并转发给对应的服务
3. 意图解析服务分析用户问题，识别用户意图
4. 宝可梦数据服务从PokeAPI获取相关宝可梦数据
5. 图鉴问答服务整合宝可梦数据，调用豆包API生成回答
6. API路由层将回答返回给用户

## 部署与运行

1. 安装依赖: `pip install -r requirements.txt`
2. 配置环境变量: 复制.env.example为.env并填写相关配置
3. 启动应用: `python main.py`
4. 访问API文档: http://localhost:8000/docs