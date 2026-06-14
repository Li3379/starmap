"""FastAPI 应用入口。

启动：uvicorn app.main:app --reload
文档：http://localhost:8000/docs （Swagger，自动从路由生成，对应契约一致性校验）
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化连接，关闭时释放。"""
    logger.info("StarMap 启动中... env={}", settings.app_env)
    # TODO(W1-W2): 在此初始化 Neo4j/PG/Redis/Chroma 连接池
    # TODO(W1-W2): 启动时校验 openapi 与 /contracts/openapi.yaml 一致（规范1）
    yield
    logger.info("StarMap 关闭中...")


app = FastAPI(
    title="星图 StarMap API",
    description="人才能力星云导航系统 - 后端 API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS：允许前端开发端口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 v1 路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["系统"])
async def health() -> dict:
    """健康检查端点（§3.2 L1 日志监控要求）。"""
    return {"status": "ok", "version": "0.1.0", "env": settings.app_env}
