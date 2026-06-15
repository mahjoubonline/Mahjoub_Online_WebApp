# 📂 apps/utils/bridge_engine.py
import requests
import logging

logger = logging.getLogger(__name__)

class QumraBridgeEngine:
    def __init__(self):
        self.url = "https://mahjoub.online/admin/graphql"
        self.token = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"

    def execute_query(self, query):
        """تنفيذ استعلام GraphQL مع معالجة الأخطاء للاتصال"""
        try:
            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                json={"query": query},
                timeout=15 # أضفنا تايم أوت لكي لا يعلق النظام للأبد
            )
            
            # تحقق من حالة الرد
            if response.status_code == 200:
                result = response.json()
                # التحقق إذا كان هناك أخطاء داخل رد الـ GraphQL نفسه
                if "errors" in result:
                    logger.error(f"GraphQL Errors: {result['errors']}")
                return result
            else:
                logger.error(f"Bridge HTTP Error: {response.status_code} - {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Bridge Connection Error: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Bridge Unexpected Error: {str(e)}")
            return {}
