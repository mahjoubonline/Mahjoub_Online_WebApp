# core/services/supplier_service.py
from core import db
from core.models.supplier import Supplier
import logging

# إعداد السجلات لمراقبة العمليات السيادية
logger = logging.getLogger(__name__)

def update_supplier_profile(supplier_id, data):
    """
    بروتوكول تحديث بيانات الكيان مع نظام تتبع (Debug) لحل مشكلة عدم الحفظ.
    """
    try:
        # 🟢 تتبع: رؤية البيانات القادمة من المتصفح في سجلات Railway
        logger.info(f"🔍 محاولة تحديث المورد {supplier_id}. البيانات المستلمة: {data}")

        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            logger.warning(f"❌ الكيان {supplier_id} غير موجود في القاعدة.")
            return False, "عذراً، لم يتم العثور على الكيان."

        # تحديث الحقول مع التأكد من وجود القيمة في 'data'
        if 'trade_name' in data:
            supplier.trade_name = data.get('trade_name')
        if 'owner_name' in data:
            supplier.owner_name = data.get('owner_name')
        if 'email' in data:
            supplier.email = data.get('email')
        if 'phone' in data:
            supplier.phone = data.get('phone')
        
        # إضافة حقول إضافية قد تكون ناقصة في الواجهة
        if 'province' in data:
            supplier.province = data.get('province')
        if 'district' in data:
            supplier.district = data.get('district')

        if 'identity_image' in data and data['identity_image']:
            supplier.identity_image = data.get('identity_image')

        # 🟢 تعميد التعديلات
        db.session.commit()
        
        # تتبع بعد الحفظ للتأكد من نجاح العملية في PostgreSQL
        logger.info(f"✅ تم الحفظ بنجاح للكيان: {supplier.trade_name}")
        return True, "تم تحديث بيانات الكيان بنجاح."
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"⚠️ فشل تحديث بيانات المورد {supplier_id}: {str(e)}")
        return False, str(e)

# بقية الدوال (get_all_suppliers, create_supplier, get_next_supplier_id) تبقى كما هي دون تغيير
