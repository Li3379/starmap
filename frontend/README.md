# 前端 README

## 启动（开发）

```bash
docker-compose -f docker-compose.dev.yml up frontend
# 访问 http://localhost:5173
```

## 本地直接运行

```bash
cd frontend
npm install
npm run gen:api   # 从 starmap-contracts/openapi.yaml 生成 TS 类型
npm run dev
```

## 命令

| 命令 | 作用 |
|------|------|
| `npm run dev` | 开发服务器（HMR）|
| `npm run build` | 构建（含 typecheck）|
| `npm run typecheck` | TS 类型检查（CI 门禁）|
| `npm run lint` | ESLint（CI 门禁）|
| `npm run test` | Vitest 单测 |
| `npm run gen:api` | 从契约生成 API 类型（规范1 双端类型一致）|

## Mock 优先（规范4 §17.5）

`src/mock/handlers.ts` 用 MSW 拦截请求返回样例，流C 从 W3 起独立开发。
真实接口在 W6 联调时切换（去掉 main.ts 里的 mock 启用）。

## 关键依赖

- Vue 3 + TypeScript + Vite
- Element Plus（UI 组件库）
- AntV G6 5.x（图谱可视化）
- ECharts（雷达/趋势/热力图）
- Pinia（状态管理）
- MSW（Mock）
