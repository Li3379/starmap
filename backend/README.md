# 后端 README

## 启动（开发）

```bash
# 在项目根目录
docker-compose -f docker-compose.dev.yml up backend
# 访问 http://localhost:8000/docs 查看 Swagger
```

## 本地直接运行（不用 Docker 时）

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

## 测试

```bash
cd backend
poetry run pytest              # 含覆盖率（门禁 60%）
poetry run ruff check .        # lint
poetry run mypy app            # type check
```

## 目录结构

```
backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置（pydantic-settings）
│   ├── dependencies.py      # 依赖注入
│   ├── api/v1/              # 路由层（对应契约 openapi.yaml）
│   ├── core/                # 核心业务逻辑
│   │   ├── extraction/      # 信息抽取引擎（流B）
│   │   ├── trust/           # 信任度模型（流B）
│   │   ├── hallucination/   # 幻觉防控（流B）
│   │   ├── graph_engine/    # 图谱引擎（流A）
│   │   ├── evolution/       # 演化分析（流B）
│   │   └── matching/        # 匹配引擎（流B）
│   ├── models/              # ORM / Schema（流B 收归，规范2）
│   ├── services/            # 数据服务封装（Neo4j/PG/Chroma/Redis/LLM）
│   ├── tasks/               # Celery 异步任务
│   └── utils/
├── tests/
├── alembic/                 # 迁移（规范2：模型变更必走）
├── pyproject.toml           # Poetry 依赖（poetry.lock 锁定，规范3）
└── Dockerfile.dev
```

## 规范提醒

- **契约优先**（§17.2）：改接口字段先改 `starmap-contracts/openapi.yaml`，发 PR，签字后改代码
- **模型变更管制**（§17.3）：改库走 `alembic revision --autogenerate`，禁止手动改库
- **Docker 开发**（§17.4）：依赖锁死版本，禁止裸 `pip install`
