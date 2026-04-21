"""
=============================================================================
文件: app/schemas/lawyer.py
模块: 律师数据模式
描述: 律师列表项、详情响应，与前端 allLawyers / lawyerInfo 对齐
=============================================================================
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict


class LawyerListItem(BaseModel):
    """律师列表项，与前端 allLawyers 项一致。"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    title: Optional[str] = None
    avatarEmoji: Optional[str] = None
    introduction: Optional[str] = None
    tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None


class LawyerStats(BaseModel):
    """律师统计数据（前端 stats）。"""
    caseCount: Optional[str] = None
    winRate: Optional[str] = None
    clientSatisfaction: Optional[str] = None
    years: Optional[str] = None


class LawyerEducation(BaseModel):
    """教育背景。"""
    degree: Optional[str] = None
    school: Optional[str] = None
    major: Optional[str] = None


class LawyerDetailOut(BaseModel):
    """律师详情，与前端 lawyerInfo 对齐。"""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    title: Optional[str] = None
    avatarEmoji: Optional[str] = None
    organization: Optional[str] = None
    licenseNumber: Optional[str] = None
    practiceYears: Optional[str] = None
    practiceArea: Optional[str] = None
    expertise: Optional[str] = None
    stats: Optional[LawyerStats] = None
    education: Optional[Dict] = None
    languageSkills: Optional[str] = None
    introduction: Optional[str] = None
    expertiseAreas: Optional[List[str]] = None
    workExperience: Optional[List[Dict]] = None
    caseExperience: Optional[List[Dict]] = None
