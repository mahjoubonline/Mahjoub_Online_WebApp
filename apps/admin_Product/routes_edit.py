# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

from flask import render_template, request, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

# استعلام جلب تفاصيل منتج واحد بناءً على هيكل Schema قمرة الصحيح
FIND_PRODUCT_QUERY = """
query GetProduct($qid: String!) {
  findProductByQid(qid: $qid) {
    success
    message
    data {
      qid
      title
      pricing { price }
      quantity
      images { fileUrl }
      identification { sku }
    }
  }
}
"""

@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """جلب بيانات المنتج من قمرة وعرضها في صفحة التعديل"""
    # فك ترميز الـ qid لأن الرابط قد يحتوي على رموز مرمزة
    clean_qid = unquote(unquote(qid))
    
    try:
        # إرسال الاستعلام مع التأكد من نوع المتغير String!
        variables = {"qid": clean_qid}
        response = QomrahGraphQLClient.execute_query(FIND_PRODUCT_QUERY, variables)
        
        product = {}
        # استخراج البيانات من استجابة GraphQL بناءً على هيكل النظام الجديد
        if response and 'data' in response:
            result = response['data'].get('findProductByQid', {})
            
            if result.get('success'):
                product = result.get('data', {})
            else:
                error_msg = result.get('message', "لم يتم العثور على المنتج في قمرة.")
                logger.warning(f"⚠️ {error_msg} لـ qid: {clean_qid}")
                flash(error_msg)
        else:
            flash("خطأ في الاتصال بخادم البيانات.")
            
        # إرسال البيانات للقالب. القالب مهيأ للتعامل مع قاموس فارغ إذا فشل الجلب
        return render_template('admin/admin_edit_product.html', product=product)
        
    except Exception as e:
        logger.error(f"❌ خطأ في جلب تفاصيل المنتج {clean_qid}: {str(e)}")
        flash("حدث خطأ تقني أثناء تحميل بيانات المنتج.")
        return render_template('admin/admin_edit_product.html', product={})
