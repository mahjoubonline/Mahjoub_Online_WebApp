# apps/services/product_sync_service.py

import requests

GRAPHQL_ENDPOINT = "https://your-external-store.com/graphql"

class ProductSyncService:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def fetch_products(self, page: int = 1, limit: int = 20):
        query = """
        query($page: Int!, $limit: Int!) {
          findAllProducts(input: { page: $page, limit: $limit }) {
            success
            message
            data {
              id
              title
              description
              price
              sku
            }
            currency {
              code
              symbol
            }
            pagination {
              total
              page
              limit
            }
          }
        }
        """

        variables = {"page": page, "limit": limit}
        response = requests.post(
            GRAPHQL_ENDPOINT,
            headers=self.headers,
            json={"query": query, "variables": variables}
        )

        result = response.json()
        return result["data"]["findAllProducts"]

    def sync_to_local_db(self, products_data):
        # هنا تكتب منطق حفظ المنتجات في قاعدة بياناتك الداخلية
        for product in products_data["data"]:
            print(f"Syncing product {product['id']} - {product['title']}")
            # مثال: تحديث أو إدخال المنتج في جدول المنتجات
            # db.upsert_product(product)

        print("Sync completed successfully.")
