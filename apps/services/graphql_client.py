import requests
import os
import logging
import urllib3
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QomrahGraphQLClient:
    BASE_URL = "https://api.qomrah.com/graphql"
    
    @staticmethod
    def _get_headers(extra_headers=None):
        api_key = os.environ.get('QUMRA_API_KEY')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Connection": "keep-alive"
        }
        # دمج الترويسات الإضافية (مثل X-Apollo-Operation-Name) إذا وُجدت
        if extra_headers:
            headers.update(extra_headers)
        return headers

    @staticmethod
    def fetch_products(headers=None): # إضافة headers هنا لحل مشكلة unexpected keyword argument
        query = "query { findAllProducts { _id title price sku } }"
        
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=3))
        
        try:
            # استخدام الترويسات الممررة من الـ route مع الترويسات الأساسية
            final_headers = QomrahGraphQLClient._get_headers(extra_headers=headers)
            
            response = session.post(
                QomrahGraphQLClient.BASE_URL,
                json={'query': query},
                headers=final_headers,
                verify=False,
                timeout=20
            )
            if response.status_code == 200:
                return response.json().get('data', {}).get('findAllProducts', [])
            else:
                logging.error(f"خطأ HTTP: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logging.error(f"فشل الاتصال: {str(e)}")
            return []
