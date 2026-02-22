#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建表结构并插入示例数据
"""

import os
import sys
from datetime import date, datetime, timezone

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.db.session import engine, init_db
from app.db.base import Base
from app.models.user import User
from app.models.case import Case

# 简化版密码哈希函数，避免循环导入
import bcrypt
def get_password_hash(password: str) -> str:
    """简化版密码哈希函数"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def init_database():
    """初始化数据库并插入示例数据"""
    print("初始化数据库...")
    
    # 初始化数据库表结构
    init_db()
    
    # 创建数据库会话
    from app.db.session import SessionLocal
    db: Session = SessionLocal()
    
    try:
        # 检查是否已有用户数据
        user_count = db.query(User).count()
        if user_count > 0:
            print("数据库中已有用户数据，跳过示例数据插入")
            return
        
        # 创建示例用户
        print("创建示例用户...")
        
        # 律师用户
        lawyer = User(
            username="张律师",
            email="zhang@lawfirm.com",
            hashed_password=get_password_hash("lawyer123"),
            is_active=True,
            role="lawyer",
            avatar="https://example.com/avatar1.jpg",
            phone="13800138001",
            created_at=datetime.now(timezone.utc)
        )
        db.add(lawyer)
        
        # 客户用户
        client = User(
            username="李客户",
            email="li@company.com",
            hashed_password=get_password_hash("client123"),
            is_active=True,
            role="client",
            avatar="https://example.com/avatar2.jpg",
            phone="13800138002",
            created_at=datetime.now(timezone.utc)
        )
        db.add(client)
        
        # 提交用户数据
        db.commit()
        db.refresh(lawyer)
        db.refresh(client)
        
        # 创建示例案件
        print("创建示例案件...")
        
        case1 = Case(
            case_no="(2024)京0105民初1234号",
            title="某某科技公司与某某个人技术服务合同纠纷案",
            case_type="合同纠纷",
            status="processing",
            progress=60,
            court="北京市朝阳区人民法院",
            judge="王法官",
            filing_date=date(2024, 3, 15),
            amount="500000",
            applicable_law="《中华人民共和国民法典》第五百零九条",
            lawyer_id=lawyer.id,
            client_id=client.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(case1)
        
        case2 = Case(
            case_no="(2024)沪0115民初5678号",
            title="某某电商平台与某某商家合作协议纠纷案",
            case_type="合同纠纷",
            status="pending",
            progress=20,
            court="上海市浦东新区人民法院",
            judge="李法官",
            filing_date=date(2024, 4, 1),
            amount="1200000",
            applicable_law="《中华人民共和国民法典》第六百零一条",
            lawyer_id=lawyer.id,
            client_id=client.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(case2)
        
        case3 = Case(
            case_no="(2023)粤0306民初9999号",
            title="某某软件公司与某某员工劳动合同纠纷案",
            case_type="劳动争议",
            status="completed",
            progress=100,
            court="深圳市南山区人民法院",
            judge="陈法官",
            filing_date=date(2023, 12, 1),
            amount="300000",
            applicable_law="《中华人民共和国劳动合同法》第三十八条",
            lawyer_id=lawyer.id,
            client_id=client.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(case3)
        
        # 提交案件数据
        db.commit()
        
        print("数据库初始化完成！")
        print(f"创建了 {2} 个用户和 {3} 个案件")
        
    except Exception as e:
        print(f"初始化过程中出现错误: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()