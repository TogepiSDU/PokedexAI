# Pokédex AI 智能图鉴系统 v1.1

一个基于AI技术的智能宝可梦图鉴系统，提供宝可梦信息查询、智能问答等功能。

> **重要提示**：当前版本仅支持宝可梦特性和种族值的查询功能，进化链及其他相关服务暂未在问答逻辑中实现，计划在后续版本中更新。

## 📋 功能特性

- **宝可梦信息查询**：获取宝可梦的详细信息，包括属性、特性、种族值等
- **智能问答系统**：基于AI的宝可梦相关问题回答，支持特性和种族值查询
- **意图识别**：自动识别用户查询意图和宝可梦名称
- **RESTful API**：提供标准化的API接口，主要包含`/ask`问答接口和`/health`健康检查接口
- **数据持久化**：使用MySQL数据库存储宝可梦信息，支持数据缓存

## 🛠 技术栈

- **后端框架**：FastAPI
- **编程语言**：Python 3.9+
- **数据库**：MySQL
- **ORM**：SQLAlchemy
- **AI模型**：豆包API
- **宝可梦数据**：PokeAPI
- **异步支持**：支持异步API请求和处理

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip

### 安装步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd PokedexAI
```

2. **创建虚拟环境**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

复制 `.env.example` 文件并命名为 `.env`，然后根据需要修改配置：

```bash
cp .env.example .env
```

主要配置项：

```
# 应用配置
APP_NAME=Pokédex AI
APP_VERSION=1.0.0
DEBUG=True

# 数据库配置 (MySQL)
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/pokedex

# 豆包AI配置
DOUBAO_API_KEY=your_api_key
DOUBAO_API_BASE_URL=https://api.doubao.com/

# PokeAPI配置
POKEAPI_BASE_URL=https://pokeapi.co/api/v2/
POKEAPI_TIMEOUT=10
```

5. **运行应用**

```bash
python main.py
```

6. **访问应用**

- API文档：http://localhost:8000/docs
- 应用地址：http://localhost:8000

## 📁 项目结构

```
PokedexAI/
├── app/                    # 主应用目录
│   ├── api/               # API路由层
│   ├── clients/           # 外部服务客户端
│   ├── core/              # 核心配置
│   ├── db/                # 数据库相关
│   ├── repositories/      # 数据访问层
│   ├── schemas/           # 数据模型
│   ├── services/          # 业务逻辑层
│   └── utils/             # 工具函数
├── docs/                  # 文档目录
├── tests/                 # 测试目录
├── .env.example           # 环境变量示例
├── .gitignore             # Git忽略文件
├── main.py                # 应用入口
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明文档
```

## 📖 使用说明

### API接口

#### 智能问答接口

```
POST /ask
```

请求体：

```json
{
  "question": "皮卡丘的属性和种族值是什么？"
}
```

响应：

```json
{
  "answer": "皮卡丘是电属性的宝可梦，种族值总和为320...",
  "pokemon_name": "pikachu",
  "pokemon_id": 25,
  "intent": {
      "pokemon_name": "pikachu",
      "original_name": "皮卡丘",
      "intent_type": "basic_info",
      "detail_level": "normal"
  }
}```

#### 健康检查接口

```
GET /health
```

响应：

```json
{
  "status": "healthy",
  "timestamp": "2025-11-14T12:00:00Z"
}```

### 功能限制说明

当前版本（v1.0）支持以下问题类型：
- 宝可梦的属性查询
- 宝可梦的种族值查询
- 宝可梦的特性查询
- 宝可梦的基本信息查询（身高、体重等）

**限制**：关于进化链的问题可能返回有限信息，因为当前问答逻辑未完全集成进化链数据。
```

## 🧪 测试

运行测试：

```bash
pytest tests/
```

## 📚 文档

- [文档目录](docs/文档目录.md) - 所有文档的导航索引
- [API文档](docs/API文档.md) - 详细的API接口说明
- [技术方案设计文档](docs/《Pokédex AI 智能图鉴系统》技术方案设计文档（TDD）.md)
- [需求文档](docs/《Pokédex AI 智能图鉴系统》需求文档（PRD）.md)
- [技术文档](docs/tech-doc.md) - 后端技术架构详细文档
- [版本迭代记录](docs/版本迭代记录.md) - 版本历史和后续规划

## 🔧 开发指南

### 代码规范

- 使用 PEP 8 代码风格
- 编写详细的函数文档注释
- 为关键功能编写单元测试

### 提交规范

- 提交信息应清晰描述修改内容
- 遵循 Conventional Commits 规范

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请联系项目维护者。

---

© zsr0411@yeah.net