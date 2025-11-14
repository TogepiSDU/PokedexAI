# Pokédex AI 智能图鉴系统 v1.0

一个基于AI技术的智能宝可梦图鉴系统，提供宝可梦信息查询、智能问答等功能。

## 📋 功能特性

- **宝可梦信息查询**：获取宝可梦的详细信息，包括属性、能力、进化链等
- **智能问答系统**：基于AI的宝可梦相关问题回答
- **意图识别**：自动识别用户查询意图
- **RESTful API**：提供标准化的API接口
- **数据持久化**：使用数据库存储宝可梦信息

## 🛠 技术栈

- **后端框架**：FastAPI
- **编程语言**：Python 3.9+
- **数据库**：SQLite (默认)
- **ORM**：SQLAlchemy
- **AI模型**：豆包API
- **宝可梦数据**：PokeAPI

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

# 数据库配置
DATABASE_URL=sqlite:///./pokedex.db

# 豆包AI配置
DOUBAO_API_KEY=your_api_key
DOUBAO_API_SECRET=your_api_secret

# PokeAPI配置
POKEAPI_BASE_URL=https://pokeapi.co/api/v2/
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
POST /api/ask
```

请求体：

```json
{
  "question": "皮卡丘的属性是什么？"
}
```

响应：

```json
{
  "answer": "皮卡丘是电属性的宝可梦。",
  "intent": "attribute_query"
}
```

#### 宝可梦信息查询

```
GET /api/pokemon/{name}
```

响应：

```json
{
  "name": "pikachu",
  "chinese_name": "皮卡丘",
  "types": ["electric"],
  "height": 4,
  "weight": 60,
  "abilities": ["static", "lightning-rod"]
}
```

## 🧪 测试

运行测试：

```bash
pytest tests/
```

## 📚 文档

- [技术方案设计文档](docs/《Pokédex AI 智能图鉴系统》技术方案设计文档（TDD）.md)
- [需求文档](docs/《Pokédex AI 智能图鉴系统》需求文档（PRD）.md)
- [项目结构文档](docs/PROJECT_STRUCTURE.md)

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