# 星图 StarMap —— 人才能力星云导航系统

> 赛题：XH-202621 多源异构数据驱动岗位与能力图谱构建与动态演化分析研究
> 发榜单位：科大讯飞股份有限公司

## 这是什么

构建新一代信息技术领域岗位能力知识图谱，支持新岗位发现、既有岗位能力动态更新、全景图谱可视化、人岗匹配诊断。详见 `星图-项目设计文档.docx`。

## 快速开始（开发环境）

```bash
# 1. 克隆
git clone <repo-url> starmap
cd starmap

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 XUNFEI_API_KEY 等

# 3. 一键启动全栈（规范3：开发也用 Docker）
docker-compose -f docker-compose.dev.yml up
```

服务地址：
- 前端：http://localhost:5173
- 后端 API 文档：http://localhost:8000/docs
- Neo4j 浏览器：http://localhost:7474 （neo4j / starmap123456）

## 项目结构

```
starmap/
├── backend/                # FastAPI 后端（流A/流B）
├── frontend/               # Vue 3 前端（流C）
├── crawler/                # 爬虫模块（流A）
├── evaluation/             # 评估脚本 + Golden Set（流D）
├── starmap-contracts/      # 接口契约（单一事实源，规范1）
├── docker-compose.dev.yml  # 开发环境编排
├── .github/workflows/      # CI 流水线
└── .env.example            # 环境变量模板
```

## 工作流（文档 §11.2）

| 流 | 组 | 范围 |
|----|----|------|
| A | 后端组 | 数据采集→图谱服务→API→部署 |
| B | 算法组 | 抽取→归一化→演化→匹配 |
| C | 前端组 | 组件库→图谱页→匹配页→看板 |
| D | QA | 评估方法学→Golden标注→评分→达标 |

优先级（D8 决策）：**D > B > A > C**

## 强制协作纪律（§17，🔴全员遵守）

1. **契约优先**：先改 `starmap-contracts/`，签字后再写代码
2. **模型变更管制**：走 Alembic 迁移，权限收归技术负责人+算法负责人
3. **Docker 开发**：依赖锁死版本（poetry.lock / package-lock.json）
4. **Mock 优先**：流C 用 MSW 独立开发，不依赖流B
5. **Trunk-based**：main 始终可运行，分支 ≤3天，PR 需 CI全绿+1人review
6. **进度可视**：任务进 GitHub Projects 看板，决策落文档附录D
7. **每日集成**：远程服务器每日拉main跑冒烟，当天问题当天修

**3 条永不可松绑的铁律**：① 契约优先 ② main 可运行 ③ 每日集成

## 文档

- [设计文档](../星图-项目设计文档.docx) —— 总纲
- [后端 README](backend/README.md)
- [前端 README](frontend/README.md)
- [接口契约](starmap-contracts/README.md)
