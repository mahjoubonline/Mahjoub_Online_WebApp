# coding: utf-8
# 📂 apps/orders/routes.py - لوحة تحكم الطلبات والعمليات (النسخة النهائية)

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from apps.models.orders_db import ProcessedOrder, OrderItem
from apps.api.sync_engine import SyncEngine
from apps.extensions import db
import logging

# تعريف الـ Blueprint
orders_blueprint = Blueprint('orders', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

@orders_blueprint.route('/dashboard', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض لوحة التحكم مع جلب الطلبات بكامل تفاصيلها"""
    try:
        # جلب الطلبات مرتبة من الأحدث للأقدم
        orders = ProcessedOrder.query.order_by(ProcessedOrder.processed_at.desc()).all()
        return render_template('admin/orders_dashboard.html', orders=orders)
    
    except Exception as e:
        logger.error(f"❌ [Dashboard Error] فشل تحميل الطلبات: {e}")
        flash("تعذر تحميل الطلبات، يرجى التحقق من اتصال قاعدة البيانات.", "danger")
        return render_template('admin/orders_dashboard.html', orders=[])

@orders_blueprint.route('/sync/<order_id>', methods=['POST'])
@login_required
def manual_sync(order_id):
    """زر المزامنة اليدوية: يقوم بجلب تفاصيل الطلب من قمرا وتحديثه"""
    try:
        # استدعاء المحرك لجلب البيانات وتحديثها
        success = SyncEngine.fetch_and_sync_order(order
