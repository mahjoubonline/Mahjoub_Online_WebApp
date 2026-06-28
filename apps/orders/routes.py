# coding: utf-8
# 📂 apps/orders/routes.py

import os
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.orders.services import OrderService

# تعريف الـ Blueprint
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/dashboard')
@login_required
def dashboard():
    """عرض لوحة تحكم الطلبات مع الإحصائيات."""
    
    # 1. جلب كافة السجلات المالية لحساب الإجمالي
    all_financials = OrderFinancial.query.all()
    total_sales = sum(f.total_paid for f in all_financials)
    
    # 2. حساب إحصائيات الطلبات
    stats = {
        'cancelled': Order.query.filter_by(status='cancelled').count(),
        'completed': Order.query.filter_by(status='completed').count(),
        'total_sales': float(total_sales)
    }
    
    # 3. جلب قائمة الطلبات مع بياناتها المالية (Join)
    # نستخدم join للحصول على البيانات المالية المرتبطة بكل طلب
    items = db.session.query(Order, OrderFinancial)\
        .join(OrderFinancial, Order.id == OrderFinancial.order_id)\
        .order_by(Order.id.desc()).all()
    
    return render_template('admin/orders_dashboard.html', stats=stats, items=items)

@orders_bp.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """دالة تشغيل المزامنة اليدوية باستخدام مفتاح البيئة الآمن."""
    
    # جلب المفتاح من إعدادات Render (المتغير الذي أضفناه سابقاً)
    api_key = os.environ.get("QUMRA_API_KEY")
    
    if not api_key:
        flash("خطأ: مفتاح الـ API غير معرف في إعدادات النظام", "danger")
        return redirect(url_for('orders.dashboard'))

    # استدعاء الخدمة
    success = OrderService.fetch_and_sync_orders(api_key=api_key, supplier_id=1)
    
    if success:
        flash("تمت المزامنة وتحديث البيانات بنجاح", "success")
    else:
        flash("حدث خطأ أثناء المزامنة، يرجى مراجعة سجلات الخطأ", "danger")
        
    return redirect(url_for('orders.dashboard'))

@orders_bp.route('/view-order/<string:order_id>') # تم تغييرها لـ string لأن معرفات قمرة قد تكون نصوصاً
@login_required
def view_order(order_id):
    """عرض تفاصيل طلب محدد."""
    result = db.session.query(Order, OrderFinancial)\
        .filter(Order.id == order_id)\
        .join(OrderFinancial, Order.id == OrderFinancial.order_id).first_or_404()
        
    return render_template('admin/order_details.html', order=result[0], financial=result[1])
