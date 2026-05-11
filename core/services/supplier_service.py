# core/services/supplier_service.py
from core import db
from core.models.supplier import Supplier

def create_new_supplier(data):
    """
    محرك الأرشفة: يستقبل البيانات الخام ويحولها لمورد معمد في قاعدة البيانات
    """
    try:
        # 1. تجهيز الكيان
        new_supplier = Supplier(
            username=data.get('username'),
            trade_name=data.get('trade_name'),
            owner_name=data.get('owner_name'),
            activity_type=data.get('activity_type'),
            identity_type=data.get('identity_type'),
            phone=data.get('phone'),
            email=data.get('email'),
            province=data.get('province'),
            district=data.get('district'),
            address_detail=data.get('address_detail'),
            bank_name=data.get('bank_name'),
            bank_acc=data.get('bank_acc')
        )

        # 2. تفعيل الحماية والأكواد السيادية
        new_supplier.set_password(data.get('password', '123456'))
        new_supplier.generate_sovereign_codes()

        # 3. الحفظ
        db.session.add(new_supplier)
        db.session.commit()
        
        return True, new_supplier
    except Exception as e:
        db.session.rollback()
        return False, str(e)
