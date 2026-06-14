"""岗位管理 API（占位）。对应模块A/B（§5.1/§5.2），W5-W8 流B 实现。"""
from fastapi import APIRouter

router = APIRouter(prefix="/positions", tags=["岗位管理"])


@router.get("/")
async def list_positions():
    """岗位列表。"""
    return {"items": []}


@router.post("/discover")
async def discover_position():
    """触发新岗位发现流程（模块A）。TODO(W7): 编排涌现检测→聚类→定义生成→幻觉防控。"""
    return {"message": "TODO"}
