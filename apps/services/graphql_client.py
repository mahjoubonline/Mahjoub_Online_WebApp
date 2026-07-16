# coding: utf-8
# 📂 apps/services/graphql_client.py

import requests
import os
import logging
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QomrahGraphQLClient:
    # الرابط الجديد المعتمد للمزامنة
    BASE_URL = "https://mahjoub.online/admin/graphql"
    
    @staticmethod
    def _get_session():
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    @staticmethod
    def execute_query(query, variables=None):
        api_key = os.environ.get('QUMRA_API_KEY')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        
        session = QomrahGraphQLClient._get_session()
        try:
            response = session.post(
                QomrahGraphQLClient.BASE_URL,
                json={'query': query, 'variables': variables},
                headers=headers,
                verify=False,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if 'errors' in result:
                logging.error(f"GraphQL Errors: {result['errors']}")
                return None
            return result.get('data')
            
        except Exception as e:
            logging.error(f"خطأ الاتصال بـ {QomrahGraphQLClient.BASE_URL}: {str(e)}")
            return None
