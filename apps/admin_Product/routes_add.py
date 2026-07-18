# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
# الاستيراد الصحيح للـ Blueprint من ملف الـ registry المركزي
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    صفحة إضافة منتج جديد.
    - في حالة GET: نعرض نموذج الإضافة.
    - في حالة POST: نقوم بمعالجة البيانات (إذا كنت سترسلها عبر AJAX).
    """
    if request.method == 'GET':
        return render_template('admin/add_product.html')

    # إذا كان هناك منطق POST لمعالجة الإضافة
    # يمكننا إضافة منطق GraphQL هنا لاحقاً
    return jsonify({"status": "error", "message": "لم يتم تفعيل الإضافة بعد"})

# ملاحظة: تأكد أن القالب موجود في المسار:
# apps/admin_Product/templates/admin/add_product.html
