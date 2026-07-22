# coding: utf-8
# 📂 apps/services/fetch_product_data.graphql.py

GET_PRODUCT_DETAIL_QUERY = """
query GetAllProductData($qid: String!) {
  findProductByQid(qid: $qid) {
    success
    message
    data {
      qid
      title
      slug
      description
      status
      quantity
      trackQuantity
      allowBackorder
      views
      reviewsCount
      averageRating
      publishedAt
      tags
      images { _id fileUrl }
      pricing { price compareAtPrice costPrice currency }
      variants { 
        _id 
        sku 
        quantity 
        pricing { price compareAtPrice } 
      }
      options { name values }
      dimensions { length width height unit }
      weight { value unit }
      collections { qid title slug }
    }
  }
}
"""
