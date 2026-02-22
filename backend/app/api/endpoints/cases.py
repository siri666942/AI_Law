"""
=============================================================================
文件: app/api/endpoints/cases.py
模块: 案件接口
描述: 案件列表、详情、创建，与前端 caseList / case-detail / create-case 对接
=============================================================================
"""

import re
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_user_optional
from app.db.session import get_db
from app.models.case import Case
from app.models.user import User
from app.schemas.case import CaseCreateIn, CaseDetailOut, CaseListItem, CaseOut

router = APIRouter()


# 将过滤选项API放在最前面，确保正确的路由匹配
@router.get("/filters")
def get_filter_options(db: Session = Depends(get_db)):
    """获取过滤选项"""
    # 获取所有案件的案件类型
    case_types = db.query(Case.case_type).distinct().filter(Case.case_type.isnot(None)).all()
    case_types = [ct[0] for ct in case_types]
    
    # 获取所有案件的法院
    courts = db.query(Case.court).distinct().filter(Case.court.isnot(None)).all()
    courts = [c[0] for c in courts]
    
    # 获取所有案件的年份
    years = db.query(Case.filing_date).filter(Case.filing_date.isnot(None)).all()
    years = list(set([y[0].year for y in years]))
    years.sort(reverse=True)
    
    # 返回过滤选项
    return {
        "caseTypes": case_types if case_types else ["合同纠纷", "劳动争议", "知识产权", "公司纠纷"],
        "courts": courts if courts else ["北京市第一中级人民法院", "上海市第二中级人民法院", "深圳市中级人民法院"],
        "procedures": ["一审", "二审", "再审"],
        "years": years if years else [2024, 2023, 2022],
        "results": ["原告胜诉", "被告胜诉", "调解结案"]
    }


def _parse_filing_date(s: str | None) -> date | None:
    if not s or not s.strip():
        return None
    s = s.strip()
    # ISO: 2024-01-15
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return date.fromisoformat(s)
    # 2024年1月15日
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日?", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return date(y, mo, d)
    return None


def _status_type(status: str) -> str:
    if status == "completed":
        return "completed"
    if status == "processing":
        return "processing"
    return "pending"


def _build_list_item(case: Case, is_lawyer_view: bool) -> CaseListItem:
    status_type = _status_type(case.status)
    date_str = (
        case.filing_date.isoformat()
        if case.filing_date
        else (case.created_at.strftime("%Y-%m-%d") if case.created_at else "")
    )
    lawyer_name = case.lawyer.username if case.lawyer else ""
    client_name = case.client.username if case.client else ""
    return CaseListItem(
        id=case.id,
        caseNo=case.case_no,
        title=case.title,
        status=case.status,
        statusType=status_type,
        date=date_str,
        progress=case.progress or 0,
        type=case.case_type,
        lawyer=lawyer_name if not is_lawyer_view else None,
        client=client_name if is_lawyer_view else None,
    )


def _build_legal_case(case: Case) -> dict:
    """构建与前端LegalCase接口一致的数据结构"""
    # 这里我们使用一些示例数据来匹配前端期望的结构
    return {
        "id": str(case.id),
        "title": case.title,
        "caseNumber": case.case_no,
        "court": case.court or "",
        "caseType": case.case_type or "",
        "procedure": "一审",  # 示例数据
        "year": case.filing_date.year if case.filing_date else 2024,  # 示例数据
        "result": "原告胜诉" if case.status == "completed" else "审理中",  # 示例数据
        "parties": {
            "plaintiff": "某某公司" if case.lawyer else "",  # 示例数据
            "defendant": "某某个人" if case.client else ""  # 示例数据
        },
        "summary": f"本案涉及{case.case_type or '相关法律'}纠纷，目前正在审理中。",  # 示例数据
        "tags": [case.case_type or "法律纠纷", "民事案件"],  # 示例数据
        "date": case.filing_date.isoformat() if case.filing_date else 
                (case.created_at.strftime("%Y-%m-%d") if case.created_at else "")
    }


@router.get("", response_model=list[CaseListItem])
def list_cases(
    keyword: str | None = Query(default=None, description="搜索关键词"),
    status: str | None = Query(default=None, description="状态过滤 pending/processing/completed"),
    history: bool = Query(default=False, description="是否含已结案"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """案件列表：返回当前用户作为律师或客户参与的案件。"""
    is_lawyer_view = current_user.role == "lawyer"
    q = db.query(Case).filter(
        (Case.lawyer_id == current_user.id) | (Case.client_id == current_user.id)
    )

    if keyword:
        like = f"%{keyword}%"
        q = q.filter(Case.case_no.like(like) | Case.title.like(like))
    if status:
        q = q.filter(Case.status == status)
    if not history:
        q = q.filter(Case.status != "completed")
    q = q.order_by(Case.id.desc())
    cases = q.all()
    return [_build_list_item(c, is_lawyer_view) for c in cases]


@router.get("/legal-cases", response_model=list[dict])
def list_legal_cases(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    """案件列表：返回与前端 LegalCase 接口一致的数据结构。已登录返回其案件，未登录返回空。"""
    if not current_user:
        return []
    q = db.query(Case).filter(
        (Case.lawyer_id == current_user.id) | (Case.client_id == current_user.id)
    )
    q = q.order_by(Case.id.desc())
    cases = q.all()
    return [_build_legal_case(c) for c in cases]


@router.get("/{case_id}", response_model=CaseDetailOut)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """案件详情：仅案件律师或客户可访问。"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")
    if case.lawyer_id != current_user.id and case.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限查看该案件")
    filing_str = (
        case.filing_date.strftime("%Y年%m月%d日")
        if case.filing_date
        else (case.created_at.strftime("%Y年%m月%d日") if case.created_at else None)
    )
    return CaseDetailOut(
        id=case.id,
        caseNo=case.case_no,
        caseTitle=case.title,
        caseType=case.case_type,
        court=case.court,
        judge=case.judge,
        filingDate=filing_str,
        amount=case.amount,
        applicableLaw=case.applicable_law,
        client=case.client.username if case.client else None,
        lawyer=case.lawyer.username if case.lawyer else None,
        status=case.status,
        statusType=_status_type(case.status),
        progress=case.progress or 0,
        created_at=case.created_at,
        timeline=[],
        documents=[],
        parties=[],
    )


@router.post("", response_model=CaseOut, status_code=201)
def create_case(
    payload: CaseCreateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建案件：仅律师可创建。"""
    if current_user.role != "lawyer":
        raise HTTPException(status_code=403, detail="仅律师可创建案件")
    filing = _parse_filing_date(payload.filingDate)
    case = Case(
        case_no=payload.caseNo,
        title=payload.caseTitle,
        case_type=payload.caseType,
        court=payload.court,
        judge=payload.judge,
        filing_date=filing,
        amount=payload.amount,
        applicable_law=payload.applicableLaw,
        lawyer_id=current_user.id,
        client_id=payload.client_id,
        status="pending",
        progress=0,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return CaseOut(
        id=case.id,
        caseNo=case.case_no,
        title=case.title,
        status=case.status,
        statusType="pending",
        progress=case.progress,
        caseType=case.case_type,
        filingDate=case.filing_date.isoformat() if case.filing_date else None,
        created_at=case.created_at,
    )
