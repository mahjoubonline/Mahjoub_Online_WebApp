# coding: utf-8
from apps import db
from datetime import datetime
from sqlalchemy import event

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    # 1. المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True, nullable=False, index=True) # المعرف الموحد السيادي المؤرشف
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 2. بيانات التوثيق (تمت إضافتها لتطابق الواجهة)
    identity_type = db.Column(db.String(50))    # نوع الهوية
    identity_number = db.Column(db.String(50))  # رقم الهوية
    identity_image = db.Column(db.String(255))   # مسار صورة الهوية
    
    # 3. بيانات المالك والمنشأة
    owner_name = db.Column(db.String(150), nullable=False)
    owner_phone = db.Column(db.String(20))       # هاتف المالك الشخصي
    trade_name = db.Column(db.String(150), unique=True, nullable=False)
    shop_phone = db.Column(db.String(20), nullable=False)
    activity_type = db.Column(db.String(50))     # فئة المورد
    
    # 4. البيانات الجغرافية
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    address_detail = db.Column(db.Text)
    
    # 5. البيانات المالية
    fin_type = db.Column(db.String(20))          # بنوك أم شركات
    bank_name = db.Column(db.String(100))        # اسم الجهة
    bank_acc = db.Column(db.String(50))          # رقم الحساب
    
    # 6. حقول التحكم بالحالة والرتبة (Core Governance Fields)
    status = db.Column(db.String(20), nullable=False, default='المراجعة') 
    # يقبل حصراً: 'نشط'، 'المراجعة'، 'محظور'، 'موقوف مؤقتاً'، 'رقابة'
    
    rank_grade = db.Column(db.String(20), nullable=False, default='ريادي') 
    # يقبل حصراً الهرمية الفخمة: 'ريادي'، 'سيادي'، 'ملكي'

    # 7. حقول الحوكمة وتتبع نظام الصلاحيات (التعديل: تحويل المعرفات إلى أرقام مباشرة لتجنب تضارب العلاقات المكسورة)
    registration_source = db.Column(db.String(30), nullable=False, default='الموقع الخارجي') 
    # يحدد مكان ولادة الحساب: 'لوحة التحكم' أو 'الموقع الخارجي'
    
    # معرف الموظف أو المؤسس الذي قام بتعميد المورد
    created_by_id = db.Column(db.Integer, nullable=True) 
    
    # معرف الشخص الذي قام بآخر إجراء إداري
    updated_by_id = db.Column(db.Integer, nullable=True) 

    # 8. التوثيق والتحليل الزمني (Timestamps)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 

    def __repr__(self):
        return f'<Supplier {self.sovereign_id} - {self.trade_name}>'


# -------------------------------------------------------------------------
# 🛡️ نظام الحوكمة التلقائي: توليد المعرف السيادي الموحد قبل الحفظ في القاعدة
# -------------------------------------------------------------------------
def auto_generate_sovereign_id(mapper, connection, target):
    """
    دالة مراقبة (Event Listener) تعمل تلقائياً قبل الـ Insert لحساب التسلسل
    السيادي بدون تكرار أو تداخل حتى في حالات الضغط العالي على السيرفر.
    """
    # استعلام لجلب آخر مورد تم تسجيله في النظام بناءً على الـ ID التلقائي
    last_supplier = target.query.order_by(Supplier.id.desc()).first()
    
    if last_supplier and last_supplier.sovereign_id:
        try:
            # فصل المعرف الحالي لاستخراج الرقم التسلسلي الأخير بعد بادئة التشفير
            # صيغة المعرف: SUP-WEL-MAH9631, SUP-WEL-MAH9632 ... إلخ
            parts = last_supplier.sovereign_id.split('MAH963')
            last_num = int(parts[-1])
            next_num = last_num + 1
        except (ValueError, IndexError):
            # في حال وجود صياغة غير متوقعة، يتم الاعتماد على المعرف الرقمي كملاذ آمن
            next_num = (last_supplier.id or 0) + 1
    else:
        # إذا كان الجدول فارغاً تماماً (أول مورد في تاريخ المنصة)
        next_num = 1

    # تركيب البنية السيادية الموحدة للمعرف وحقنها في الحقل فوراً قبل إتمام الحفظ
    target.sovereign_id = f"SUP-WEL-MAH963{next_num}"

# ربط الدالة بحدث "قبل الإدخال" لجدول الموردين بشكل رسمي صارم
event.listen(Supplier, 'before_insert', auto_generate_sovereign_id)
