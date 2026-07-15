# 📂 apps/services/graphql_client.py
import requests
import os
import logging

class QomrahGraphQLClient:
    """كلاس موحد للاتصال بـ قمرة عبر GraphQL"""
    
    BASE_URL = "https://api.qomrah.com/graphql"
    
    @staticmethod
    def _get_headers(custom_headers=None):
        api_key = os.environ.get('QUMRA_API_KEY')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers

    @staticmethod
    def fetch_orders(headers=None):
        """جلب الطلبات"""
        query = """
        query {
          findAllOrders {
            _id
            customerName
            totalPrice
            tracking_tag
            items {
              productName
              quantity
              price
              sku
            }
          }
        }
        """
        response = requests.post(
            QomrahGraphQLClient.BASE_URL, 
            json={'query': query}, 
            headers=QomrahGraphQLClient._get_headers(headers)
        )
        if response.status_code == 200:
            return response.json().get('data', {}).get('findAllOrders', [])
        else:
            logging.error(f"فشل جلب الطلبات: {response.status_code} - {response.text}")
            return []

    @staticmethod
    def fetch_products():
        """جلب المنتجات"""
        query = """
        query {
          findAllProducts {
            _id
            title
            price
            sku
          }
        }
        """
        response = requests.post(
            QomrahGraphQLClient.BASE_URL, 
            json={'query': query}, 
            headers=QomrahGraphQLClient._get_headers()
        )
        if response.status_code == 200:
            return response.json().get('data', {}).get('findAllProducts', [])
        else:
            logging.error(f"فشل جلب المنتجات: {response.status_code} - {response.text}")
            return []
