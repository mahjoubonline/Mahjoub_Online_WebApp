import requests

class QmrEngine:
    def __init__(self):
        self.url = "https://mahjoub.online/admin/graphql"
        self.headers = {
            "Authorization": "Bearer qmr_79e068ae-b48a-4e8c-8481-b0cedbdee41f",
            "Content-Type": "application/json"
        }

    def execute_query(self, query, variables=None):
        """تنفيذ الاستعلامات ضد بوابة قمرة"""
        try:
            response = requests.post(
                self.url, 
                json={'query': query, 'variables': variables}, 
                headers=self.headers
            )
            return response.json()
        except Exception as e:
            print(f"❌ [QMR API Error]: {e}")
            return None

    def get_all_collections(self):
        """سحب الفئات ليختار منها المورد عند إضافة المنتج"""
        query = """
        query {
          findAllCollections {
            id
            name
          }
        }
        """
        result = self.execute_query(query)
        if result and 'data' in result:
            return result['data']['findAllCollections']
        return []
