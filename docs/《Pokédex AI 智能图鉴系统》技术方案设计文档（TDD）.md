# 《Pokédex AI 智能图鉴系统》技术方案设计文档（TDD）

- 文档版本：v1.0
- 作者：Ava
- 基于：Trae + Doubao Seed Code
- 语言环境：Python 3.x + FastAPI
- 外部依赖：PokeAPI、豆包（Doubao）

------

# 1. 系统架构概览（Architecture Overview）

本项目采用 **三层架构 + AI 工具层**：

```
┌──────────────────────────┐
│         API 层           │   ← FastAPI 路由（/ask）
└───────────────▲──────────┘
                │
┌───────────────┴──────────┐
│        业务服务层         │   ← 图鉴问答流程 orchestration
│  DexQASvc / PokemonSvc    │
└───────────────▲──────────┘
                │
┌───────────────┴──────────┐
│     数据与外部服务层      │
│ PokeAPI Client / Repository│
│ MySQL（缓存） / 豆包AI     │
└──────────────────────────┘
```

### 核心流程结构：

1. **API 层** `/ask` 接收问题
2. **AI 层（豆包）** 提取意图 → 找出宝可梦
3. **数据层** 从 MySQL 拉缓存，不足则请求 PokeAPI
4. **AI 层（豆包）** 根据结构化数据生成自然语言回答
5. 业务层组合返回给前端

------

# 2. 目录结构设计（基于 Doubao Seed Code 优化）

假设 seed code 的典型结构如下（Trae 默认）：

```
bash复制编辑/app
  /api
    router.py
  /core
    config.py
  /models
    ...
  main.py
```

我们扩展后的结构如下：

```
csharp复制编辑app/
├─ main.py                        # FastAPI 入口
├─ api/
│   ├─ router.py                  # 所有路由
│   └─ ask_api.py                 # /ask 路由定义
│
├─ services/
│   ├─ dex_qa_service.py          # 图鉴问答主流程（AI+数据）
│   ├─ pokemon_service.py         # Pokemon 数据流程服务
│   └─ intent_parser_service.py   # 豆包意图解析逻辑
│
├─ clients/
│   ├─ doubao_client.py           # 豆包 LLM 封装（解析/生成）
│   ├─ pokeapi_client.py          # 请求 PokeAPI
│   └─ http_client.py             # httpx 封装（统一请求）
│
├─ repositories/
│   ├─ pokemon_repository.py      # MySQL 数据访问层
│
├─ db/
│   ├─ base.py                    # SQLAlchemy Base
│   ├─ session.py                 # SessionLocal
│   └─ models.py                  # ORM 模型定义（Pokemon / Species）
│
├─ schemas/
│   ├─ ask_schema.py              # /ask 请求 & 响应 Schema
│   ├─ intent_schema.py           # 意图 JSON Schema
│   └─ pokemon_schema.py          # PokeAPI 数据结构 Schema（可选）
│
├─ utils/
│   ├─ name_alias.py              # 多语言/昵称映射（未来使用）
│   └─ logging.py                 # 日志格式统一
│
└─ core/
    └─ config.py                  # MySQL/LLM 密钥配置
```

> **规范性要求：**
>
> - 禁止把 AI 与 PokeAPI 逻辑写死在 API 路由中。
> - 所有业务流程必须在 `services/` 中完成。
> - 所有外部请求必须经过 `clients/`。
> - 所有数据持久化必须经过 `repositories/`。

------

# 3. 数据结构设计（MySQL + JSON 缓存）

## 3.1 MySQL 表结构（MVP）

### `pokemon` 表

| 字段       | 类型               | 说明                        |
| ---------- | ------------------ | --------------------------- |
| id         | INT PK             | PokeAPI ID                  |
| name       | VARCHAR(64) UNIQUE | 英文名（小写）              |
| data       | JSON               | `/pokemon/{name}` 原始 JSON |
| updated_at | DATETIME           | 自动更新时间                |



### `pokemon_species` 表

| 字段       | 类型               | 说明                      |
| ---------- | ------------------ | ------------------------- |
| id         | INT PK             | PokeAPI species ID        |
| name       | VARCHAR(64) UNIQUE | 英文名（小写）            |
| data       | JSON               | `/pokemon-species/{name}` |
| updated_at | DATETIME           | 自动更新时间              |



> MVP 暂不拆字段，以 JSON 为主。后续可拆表优化搜索性能。

------

# 4. 模块设计（核心部分）

以下是最关键的三个模块设计，你 coding 时会直接用上。

------

# 4.1 Intent Parser（意图解析器）

文件：`services/intent_parser_service.py`

### 输入：

```
arduino


复制编辑
"喷火龙的属性是多少"
```

### 输出（由豆包生成）：

```
json复制编辑{
  "pokemon_name": "charizard",
  "original_name": "喷火龙",
  "intent_type": "basic_info",
  "detail_level": "normal"
}
```

### 流程：

1. 拼接系统 prompt（严格要求输出 JSON）
2. 调用 `doubao_client.call_llm()`
3. JSON 解析 → schema 校验
4. 结果返回

### seed code 适配说明：

Trae 的 seed code teambox 采用 async/await 风格：

```
python


复制编辑
await doubao_client.chat(...)
```

因此意图解析需写成 async 版本：

```
python复制编辑async def parse_intent(question: str) -> IntentSchema:
    response = await doubao_client.chat(system_prompt, user_prompt)
    return IntentSchema(**json.loads(response))
```

------

# 4.2 Pokemon Service（数据获取服务）

文件：`services/pokemon_service.py`

功能：负责“先查 MySQL → 否则调 PokeAPI → 写缓存”。

### 函数：

```
python复制编辑async def get_pokemon(name: str) -> dict
async def get_species(name: str) -> dict
```

### 流程：

```
markdown复制编辑1. 统一格式化名称（小写英文名）
2. 查 MySQL（pokemon_repository）
3. 如果找到 → 返回 data
4. 如果没找到：
   - 调 PokeAPI（pokeapi_client）
   - 写入 MySQL
   - 返回 data
```

------

# 4.3 Dex QA Service（图鉴问答服务）

文件：`services/dex_qa_service.py`

这是整个 MVP 的核心 orchestrator。

### 函数

```
python


复制编辑
async def answer_question(question: str) -> dict
```

### 流程：

```
markdown复制编辑1. 调用 parse_intent() 得到宝可梦名字
2. 若为空 → 返回兜底回复
3. 用 pokemon_service 拉取：
   - pokemon
   - species
4. 组织上下文 JSON
5. 调用豆包进行回答生成（build_answer_with_doubao）
6. 返回回答
```

------

# 5. API 设计

## 5.1 `/ask`（POST）

### Request

```
json复制编辑{
  "question": "喷火龙的属性和种族值？"
}
```

### Response

```
json复制编辑{
  "answer": "喷火龙是火/飞行属性，种族值总和534...",
  "pokemon_name": "charizard",
  "pokemon_id": 6,
  "intent": {
      "pokemon_name": "charizard",
      "detail_level": "normal"
  }
}
```

------

# 6. 豆包（Doubao）调用方案设计

## 6.1 Doubao 在 Seed Code 中的使用模式

Trae seed code 通常提供：

- 异步 API 包装
- 环境变量注入（key 不写在代码里）

你需要做两种 prompt：

### 1）意图解析 Prompt（强制 JSON 输出）

系统提示：

```
javascript


复制编辑
你是宝可梦图鉴助手，只能输出 JSON...
```

用户提示：

```
javascript复制编辑用户问题：{question}
请只输出 JSON：
```

### 2）回答生成 Prompt

系统提示：

```
复制编辑
你是宝可梦专家，需要根据提供的 PokeAPI 数据组织自然语言回答...
```

用户提示为上下文 JSON。

------

# 7. HTTP Client 设计

文件：`clients/http_client.py`

- 封装 httpx，支持异步
- 支持：
  - 超时
  - 重试
  - JSON decode 错误处理

------

# 8. 错误处理和日志

## 8.1 故障点

1. PokeAPI 404
2. 豆包网络错误
3. JSON 解析失败
4. MySQL 网络异常

## 8.2 日志规范

采用结构化日志：

```
json复制编辑{
  "event": "pokeapi_fetch",
  "pokemon": "charizard",
  "status": "success"
}
```

------

# 9. 性能优化策略（MVP）

1. MySQL 缓存（避免重复访问 PokeAPI）
2. Intent Parser + Answer Generator 使用不同 prompt
3. 异步 HTTP（httpx）
4. 避免在 AI 中重复生成大段数据，数据由后端预处理

------

# 10. 后续可扩展方向

- 属性相克模块（新增 TypeService + TypeRepository）
- 多语言别名映射（name_alias）
- 全局缓存（Redis）
- UI 图鉴前端