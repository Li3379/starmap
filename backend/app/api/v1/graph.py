"""图谱查询 API（占位）。

对应文档：§3.1 L4 图谱查询服务、§8.2 app/api/v1/graph.py
契约：见 starmap-contracts/openapi.yaml 的 /graph 路径
实现里程碑：W5-W6（流A）
"""
from fastapi import APIRouter

router = APIRouter(prefix="/graph", tags=["图谱查询"])


@router.get("/panorama")
async def get_panorama(tech_stack: str | None = None, level: str | None = None):
    """全景图谱（模块C，§5.3）。支持按技术栈/级别筛选。

    TODO(W5): 返回 AntV G6 力导向图所需的 nodes/edges 结构。
    """
    return {"message": "TODO", "nodes": [], "edges": []}


@router.get("/position/{position_name}")
async def get_position_detail(position_name: str):
    """岗位详情（§8.3 岗位详情视图）。"""
    return {"message": "TODO", "position": position_name}
