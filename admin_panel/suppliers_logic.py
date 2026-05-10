# admin_panel/suppliers_logic.py
from core import db
from core.models.supplier import Supplier

class SupplierLogic:
    @staticmethod
    def register_supplier(form_data):
        """
        محرك تعميد الموردين: يستقبل البيانات من الواجهة الملكية ويحفظها في الترسانة
        """
        try:
            # 1. توليد المعرف السيادي SUP_ تلقائياً
            last_id = db.session.query(db.func.max(Supplier.id)).scalar() or 0
            new_sovereign_id = f"SUP_{last_id + 1}#"

            # 2. إنشاء كيان المورد الجديد بناءً على بيانات الواجهة
            new_supplier = Supplier(
                sovereign_id=new_sovereign_id,
                trade_name=form_data.get('trade_name'),
                owner_name=form_data.get('owner_name'),
                activity_type=form_data.get('activity_type'),
                identity_type=form_data.get('identity_type'),
                province=form_data.get('province'),
                district=form_data.get('district'),
                address_detail=form_data.get('address_detail'),
                phone=form_data.get('phone'),
                bank_name=form_data.get('bank_name'),
                bank_acc=form_data.get('bank_acc'),
                status='active'
            )

            # 3. الحفظ في قاعدة بيانات Postgres
            db.session.add(new_supplier)
            db.session.commit()

            return True, f"تم تعميد المورد {new_supplier.trade_name} بنجاح برقم {new_sovereign_id}"

        except Exception as e:
            db.session.rollback()
            print(f"❌ فشل التعميد: {str(e)}")
            return False, f"حدث خطأ أثناء التعميد: {str(e)}"

    @staticmethod
    def get_next_id():
        """دالة لتوقع الرقم التالي وإظهاره في واجهة الإضافة"""
        last_id = db.session.query(db.func.max(Supplier.id)).scalar() or 0
        return f"SUP_{last_id + 1}#"

    @staticmethod
    def search_suppliers(search_query=None, status_filter=None):
        """محرك الرادار: البحث عن الموردين وتصفيتهم"""
        query = Supplier.query
        
        if search_query:
            query = query.filter(
                (Supplier.trade_name.like(f"%{search_query}%")) |
                (Supplier.sovereign_id.like(f"%{search_query}%")) |
                (Supplier.owner_name.like(f"%{search_query}%"))
            )
        
        if status_filter:
            query = query.filter_by(status=status_filter)
            
        return query.order_by(Supplier.created_at.desc()).all()
