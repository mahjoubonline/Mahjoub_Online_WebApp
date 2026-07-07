import requests
from config import Config

class QomrahGraphQLClient:
    @staticmethod
    def get_order_details(order_id):
        query = """
        query GetOrder($id: ID!) {
            order(id: $id) {
                id
                supplier_id
                total_price
                tracking_tag
                currency
                items {
                    title
                    qty
                    subtotal
                    sku
                }
            }
        }
        """
        # إضافة المفتاح في الـ Headers
        headers = {"Authorization": f"Bearer {Config.QUMRA_API_KEY}"}
        # تنفيذ الطلب للرابط الذي حددته
        response = requests.post(
            Config.QUMRA_API_URL, 
            json={'query': query, 'variables': {'id': order_id}},
            headers=headers
        )
        return response.json().get('data', {}).get('order')
