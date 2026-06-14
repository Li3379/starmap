"""管理后台 API（占位）。对应§8.2 admin.py：人工审核队列、数据源管理、本体维护。

权限说明：评审环境单租户（§1.4.3），暂不做账号体系。
"""
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["管理后台"])


@router.get("/review-queue")
async def get_review_queue():
    """待人工审核的变更提案队列（§5.2、§7.2 防线）。"""
    return {"items": []}


@router.post("/seed/reset")
async def reset_demo_data():
    """重置为演示数据（§16.5 一键加载种子）。"""
    return {"message": "TODO"}
