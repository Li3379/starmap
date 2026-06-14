"""简历解析 API（占位）。对应§5.4 简历解析 Pipeline，W9-W10 流B 实现。

合规要点（§15）：上传简历必须经 PII 检测→脱敏→加密存储→脱敏内容传星火 API。
"""
from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/resume", tags=["简历解析"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """上传简历（PDF/Word）。返回解析后的技能列表。

    TODO(W9):
      1. 文档解析（pdfplumber/docx），失败降级 OCR（§5.4）
      2. PII 检测 + 脱敏（§15.2）
      3. LLM 技能抽取 → 归一化
    """
    return {"filename": file.filename, "skills": [], "message": "TODO"}
