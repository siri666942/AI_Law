"""
=============================================================================
文件: app/schemas/case.py
模块: 案件数据模式
描述: 案件列表、详情、创建请求的请求/响应结构，与前端 caseList/caseInfo 对齐
=============================================================================
"""

from datetime import date, datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, ConfigDict, Field


class CaseCreateIn(BaseModel):
    """创建案件请求体，与前端 create-case 表单一致。"""
    caseNo: str = Field(..., max_length=64, description="案号")
    caseTitle: str = Field(..., max_length=255, description="案件标题")
    caseType: Optional[str] = Field(default=None, max_length=64)
    court: Optional[str] = Field(default=None, max_length=255)
    judge: Optional[str] = Field(default=None, max_length=64)
    filingDate: Optional[str] = Field(default=None, description="立案时间，如 2024-01-15 或 2024年1月15日")
    amount: Optional[str] = Field(default=None, max_length=64)
    applicableLaw: Optional[str] = None
    client_id: Optional[int] = Field(default=None, alias="clientId", description="客户用户ID，可选")


class LegalCase(BaseModel):
    """案件信息，与前端 LegalCase 接口一致。"""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    caseNumber: str
    court: str
    caseType: str
    procedure: str
    year: int
    result: str
    parties: Dict
    summary: str
    tags: List[str]
    date: str


class CaseListItem(BaseModel):
    """案件列表项，与前端 caseList 项一致（camelCase 输出）。"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    caseNo: str
    title: str
    status: str
    statusType: str
    date: str
    progress: int
    type: Optional[str] = None
    lawyer: Optional[str] = None
    client: Optional[str] = None


class CaseDetailOut(BaseModel):
    """案件详情，与前端 caseInfo + 可选 timeline/documents 对齐。"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    caseNo: str
    caseTitle: str
    caseType: Optional[str] = None
    court: Optional[str] = None
    judge: Optional[str] = None
    filingDate: Optional[str] = None
    amount: Optional[str] = None
    applicableLaw: Optional[str] = None
    client: Optional[str] = None
    lawyer: Optional[str] = None
    status: str
    statusType: str
    progress: int
    created_at: Optional[datetime] = None
    timeline: Optional[List[Dict]] = None
    documents: Optional[List[Dict]] = None
    parties: Optional[List[Dict]] = None


class CaseOut(BaseModel):
    """创建案件成功返回的简要信息。"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    caseNo: str
    title: str
    status: str
    statusType: str = "pending"
    progress: int = 0
    caseType: Optional[str] = None
    filingDate: Optional[str] = None
    created_at: Optional[datetime] = None
