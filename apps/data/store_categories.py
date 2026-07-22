# coding: utf-8
# 📂 apps/data/store_categories.py

"""
قائمة فئات المتجر
"""

STORE_CATEGORIES = [
    {'id': 'electronics', 'name': 'الإلكترونيات', 'icon': 'fa-laptop'},
    {'id': 'fashion', 'name': 'الأزياء والموضة', 'icon': 'fa-tshirt'},
    {'id': 'accessories', 'name': 'الإكسسوارات', 'icon': 'fa-gem'},
    {'id': 'home', 'name': 'الأثاث المنزلي', 'icon': 'fa-couch'},
    {'id': 'kitchen', 'name': 'مستلزمات المطبخ', 'icon': 'fa-utensils'},
    {'id': 'beauty', 'name': 'التجميل والعناية', 'icon': 'fa-spa'},
    {'id': 'sports', 'name': 'الرياضة', 'icon': 'fa-running'},
    {'id': 'books', 'name': 'الكتب والمكتبات', 'icon': 'fa-book'},
    {'id': 'toys', 'name': 'الألعاب', 'icon': 'fa-gamepad'},
    {'id': 'food', 'name': 'المواد الغذائية', 'icon': 'fa-apple-alt'},
    {'id': 'health', 'name': 'الصحة', 'icon': 'fa-heartbeat'},
    {'id': 'auto', 'name': 'قطع السيارات', 'icon': 'fa-car'},
    {'id': 'construction', 'name': 'مواد البناء', 'icon': 'fa-hard-hat'},
    {'id': 'agriculture', 'name': 'الزراعة', 'icon': 'fa-seedling'},
    {'id': 'energy', 'name': 'الطاقة', 'icon': 'fa-bolt'},
    {'id': 'other', 'name': 'أخرى', 'icon': 'fa-ellipsis-h'}
]

# ✅ قائمة بأسماء الفئات فقط (للقوائم المنسدلة)
CATEGORIES_LIST = [cat['name'] for cat in STORE_CATEGORIES]

# ✅ دالة للحصول على أيقونة الفئة
def get_category_icon(category_name):
    for cat in STORE_CATEGORIES:
        if cat['name'] == category_name:
            return cat['icon']
    return 'fa-tag'

# ✅ دالة للحصول على معرف الفئة
def get_category_id(category_name):
    for cat in STORE_CATEGORIES:
        if cat['name'] == category_name:
            return cat['id']
    return None
