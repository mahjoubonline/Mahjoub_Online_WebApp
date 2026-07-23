# coding: utf-8
# 📂 apps/services/update_product_data.py

UPDATE_PRODUCT_MUTATION = """
mutation UpdateProduct($id: ID!, $input: UpdateProductInput!) {
    updateProduct(id: $id, input: $input) {
        success
        message
        data {
            qid
            title
            status
        }
    }
}
"""
