# coding: utf-8
# 📂 apps/utils/sync_manager.py

from apps.orders.services import OrderService
from apps.supplier_wallet.services import WalletService
from apps.extensions import db

class SyncManager:
    @staticmethod
    def run_sync(api_key, supplier_id):
        """
        المنسق العام: يقوم بتشغيل عملية المزامنة الشاملة.
        يستدعي OrderService لضمان تحديث الطلبات، 
        والتي بدورها تقوم بتحديث المحفظة.
        """
        try:
            # تشغيل عملية المزامنة التي قمنا ببنائها في OrderService
            # هي تقوم بجلب الطلبات + إنشاء السجلات المالية + تحديث المحفظة
            success = OrderService.fetch_and_sync_orders(api_key, supplier_id)
            
            if success:
                print(f"✅ تمت المزامنة بنجاح للمورد: {supplier_id}")
                return True
            else:
                print(f"❌ فشلت عملية المزامنة للمورد: {supplier_id}")
                return False
                
        except Exception as e:
            print(f"⚠️ خطأ غير متوقع في SyncManager: {str(e)}")
            return False
