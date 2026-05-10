# admin_panel/suppliers_logic.py
from core import db
from core.models.supplier import Supplier, archive_sys # استيراد الموديل والمحرك

class SupplierLogic:
    @staticmethod
    def register_supplier(form_data):
        """
        محرك تعميد الموردين: يستقبل البيانات من الواجهة الملكية ويحفظها في الترسانة
        """
        try:
            # 1. تجهيز المعرف السيادي SUP_
            last_id = db.session.query(db.func.max(Supplier.id)).scalar() or 0
            new_sovereign_id = f"SUP_{last_id + 1}#"

            # 2. إنشاء كيان المورد الجديد
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
                tier='مبتدئ',
                status='active'
            )

            # 3. الحفظ في قاعدة بيانات Postgres
            db.session.add(new_supplier)
            db.session.commit()

            # 4. الأرشفة السيادية إلى GitHub (بصمت)
            archive_sys.archive_entity(new_supplier)

            return True, f"تم تعميد المورد {new_supplier.trade_name} بنجاح بالرقم {new_sovereign_id}"

        except Exception as e:
            db.session.rollback()
            print(f"❌ فشل التعميد: {str(e)}")
            return False, f"حدث خطأ أثناء التعميد: {str(e)}"
