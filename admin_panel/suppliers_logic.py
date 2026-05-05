from core import db
from core.models.user import User

def get_all_pending_suppliers():
    """جلب الموردين الذين ينتظرون التعميد للمشاركة في منصة قمرة"""
    return User.query.filter_by(role='vendor', is_active_account=False).all()

def approve_supplier_sovereign(user_id):
    """بروتوكول التعميد السيادي لتفعيل المورد"""
    supplier = User.query.get(user_id)
    if supplier:
        supplier.is_active_account = True
        # هنا يمكن إضافة كود الربط البرمجي مع API قمرة مستقبلاً
        db.session.commit()
        return True
    return False
