# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة (النسخة المباشرة)

import os
import requests
import logging
from apps.extensions import db
from apps.models.sync_log import SyncLog

logger = logging.getLogger(__name__)

class SyncEngine:
    API_URL = "https://mahjoub.online/admin/graphql"  

    @staticmethod
    def _get_headers():
        api_key = os.environ.get("QUMRA_API_KEY", "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def fetch_and_sync_order():
        """
        دالة سحب الطلبات المباشرة
        """
        logger.info("🚀 محاولة سحب الطلبات مباشرة...")
        
        # استعلام يستهدف حقول الطلبات المباشرة الأكثر شيوعاً
        query = """
        query {
            findAllOrders {
                id
                totalPrice
                createdAt
                status
            }
        }
        """
        
        try:
            response = requests.post(
                SyncEngine.API_URL, 
                json={'query': query}, 
                headers=SyncEngine._get_headers(), 
                timeout=60
            )
            
            # طباعة الرد لنرى هل نجح السحب أم لا (سيكون المفتاح الأخير)
            logger.info(f"🎯 رد سحب الطلبات: {response.text}")
            
            if response.status_code == 200:
                SyncEngine._log_sync('orders', 'success', "تم تنفيذ عملية السحب بنجاح.")
                return True
            else:
                error_msg = f"فشل السحب: {response.status_code} - {response.text}"
                logger.error(f"❌ {error_msg}")
                SyncEngine._log_sync('orders', 'failed', error_msg)
                return False
                
        except Exception as e:
            err_str = str(e)
            logger.error(f"❌ خطأ فني أثناء السحب: {err_str}")
            SyncEngine._log_sync('orders', 'failed', err_str)
            return False

    @staticmethod
    def _log_sync(sync_type, status, message):
        """تسجيل العمليات في قاعدة البيانات"""
        try:
            log = SyncLog(sync_type=sync_type, status=status, error_message=message)
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()
