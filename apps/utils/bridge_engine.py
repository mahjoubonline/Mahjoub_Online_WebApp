# 📂 apps/utils/bridge_engine.py
import requests
import logging

logger = logging.getLogger(__name__)

class QumraBridgeEngine:
    def __init__(self):
        self.url = "https://mahjoub.online/admin/graphql"
        self.token = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"

    def execute_query(self, query):
        """تنفيذ أي استعلام GraphQL وإرجاع النتيجة كـ JSON"""
        try:
            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                json={"query": query}
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"GraphQL Error: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Bridge Engine Connection Error: {str(e)}")
            return {}
