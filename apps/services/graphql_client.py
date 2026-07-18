# coding: utf-8
# 📂 apps/services/graphql_queries.py

"""
🗂️ المرجع الموحد لاستعلامات ومطفرات GraphQL (Qomrah Schema Queries)
يحتوي هذا الملف على الهياكل النصية الثابتة للاتصال بقاعدة بيانات منصة قمرة.
"""

# ==========================================
# 📦 1. استعلامات قسم المنتجات (Products Queries)
# ==========================================

# جلب كافة المنتجات مع الترقيم والبحث (ProductsResponse)
GET_ALL_PRODUCTS = """
query GetAllProducts($input: GetAllProductsInput) {
  findAllProducts(input: $input) {
    data {
      qid
      title
      quantity
      pricing {
        price
      }
      images {
        fileUrl
      }
    }
    pagination {
      totalPages
      currentPage
      totalItems
    }
  }
}
"""

# جلب تفاصيل منتج محدد عبر المعرف الحصري (BaseProductResponse)
FIND_PRODUCT_BY_QID = """
query FindProductByQid($qid: String!) {
  findProductByQid(qid: $qid) {
    qid
    title
    description
    quantity
    status
    productType
    vendor
    tags
    pricing {
      price
      compareAtPrice
    }
    images {
      qid
      fileUrl
    }
  }
}
"""

# جلب الحالات المتاحة للمنتجات (findProductStatusResponse)
FIND_PRODUCT_STATUS = """
query FindProductStatus {
  findProductStatus {
    status
    count
  }
}
"""


# ==========================================
# 🛒 2. استعلامات قسم الطلبات (Orders Queries)
# ==========================================

# جلب جميع الطلبات مع الترقيم والتصفية (PaginatedOrdersResponse)
GET_ALL_ORDERS = """
query GetAllOrders($input: GetAllOrdersInput) {
  findAllOrders(input: $input) {
    data {
      qid
      orderId
      orderStatus
      financialStatus
      fulfillmentStatus
      paymentType
      totalPrice
      createdAt
    }
    pagination {
      totalPages
      currentPage
      totalItems
    }
  }
}
"""

# جلب تفاصيل طلب محدد بالكامل (OrderByIdResponse)
FIND_ORDER_BY_ID = """
query FindOrderById($qid: String!) {
  findOrderById(qid: $qid) {
    qid
    orderId
    orderStatus
    financialStatus
    fulfillmentStatus
    paymentType
    totalPrice
    taxAmount
    shippingPrice
    createdAt
    customer {
      firstName
      lastName
      phone
    }
    items {
      qid
      title
      quantity
      price
    }
  }
}
"""

# جلب خط التتبع الزمني الخاص بحالة الطلب (OrderTimelineResponse)
FIND_ORDER_TIMELINE = """
query FindOrderTimeline($orderId: String!) {
  findOrderTimeline(orderId: $orderId) {
    status
    comment
    createdAt
  }
}
"""


# ==========================================
# 📊 3. استعلامات التقارير والمالية (Analytics & Revenue)
# ==========================================

# جلب إجمالي الإيرادات والأرباح للمتجر (totalRevenueResponse)
GET_TOTAL_REVENUE = """
query GetTotalRevenue($input: AnalyticsInput) {
  totalRevenue(input: $input) {
    amount
    currency
    formattedAmount
  }
}
"""

# جلب ملخص وإحصائيات الطلبات السريعة (orderSummury / OrderStatisticsResponse)
GET_ORDER_STATISTICS = """
query GetOrderStatistics($input: AnalyticsInput) {
  orderStatistics(input: $input) {
    totalOrders
    completedOrders
    pendingOrders
    canceledOrders
  }
}
"""

# جلب الإحصائيات العامة لحساب المتجر (StatisticsApiResponse)
GET_ACCOUNT_STATISTICS = """
query GetAccountStatistics {
  findAccountStatistics {
    totalProducts
    totalCustomers
    activeVendors
  }
}
"""


# ==========================================
# 📁 4. استعلامات التصنيفات والمجموعات (Collections)
# ==========================================

# جلب جميع المجموعات المتاحة في المتجر (FindAllCollectionResponse)
GET_ALL_COLLECTIONS = """
query GetAllCollections {
  findAllCollections {
    qid
    title
    description
    slug
    image {
      fileUrl
    }
  }
}
"""

# جلب تفاصيل مجموعة محددة بالـ Qid (FindByIdollectionResponse)
FIND_COLLECTION_BY_QID = """
query FindCollectionByQid($qid: String!) {
  findCollectionByQid(qid: $qid) {
    qid
    title
    slug
  }
}
"""
