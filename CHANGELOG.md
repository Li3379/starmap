# StarMap 变更历史

格式遵循 [Keep a Changelog](https://keepachangelog.com/)。

## [Unreleased]

### Added — 阶段0：环境与仓库搭建（W1）
- 初始化 monorepo 结构（backend / frontend / crawler / evaluation / starmap-contracts）
- 后端骨架：FastAPI 入口、7 个路由占位（graph/position/match/evolution/resume/quality/admin）、健康检查、Pydantic 配置、pytest 冒烟测试
- 前端骨架：Vite + Vue3 + TypeScript、6 个占位页面、Element Plus、AntV G6、ECharts、Pinia、MSW mock
- 契约仓库 v0.1：openapi.yaml（8 个端点）、3 个共享 schema（extraction/graph_node/match_result）、Cypher 模板目录、校验脚本
- 开发环境：docker-compose.dev.yml（FastAPI/Vite/Neo4j/PostgreSQL/Redis/Chroma）
- CI 流水线：契约校验 → 后端(lint/typecheck/test) → 前端(lint/typecheck/build) → Docker 全栈冒烟
- 配置：pyproject.toml（Poetry 依赖锁定）、package.json、.env.example、.gitignore

### 决策（对应附录D）
- 本阶段执行阶段0（环境与仓库搭建），下一步进入阶段1（接口契约定义，W2 技术负责人签字）

---

> 变更规范（§17.3）：每次模型/接口/架构变更在此追加记录。
> 数据模型变更另需在 `starmap-contracts/CHANGELOG.md` 记录并群 @ 消费方。
