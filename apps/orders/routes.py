# coding: utf-8
# 📂 apps/orders/routes.py

import os
import traceback
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
# استيراد محرك المزامنة المحدث الخاص بك
from apps.api.sync_engine import SyncEngine

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
    items = db.session.query(Order, OrderFinancial)\
        .join(OrderFinancial, Order.id == OrderFinancial.order_id)\
        .order_by(Order.id.desc()).all()
    
    return render_template('admin/orders_dashboard.html', stats=stats, items=items)

@orders_bp.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """دالة المزامنة مع التقاط الأخطاء التفصيلي باستخدام المحرك الجديد."""
    
    try:
        # تشغيل محرك المزامنة الجديد
        success = SyncEngine.fetch_and_sync_order()
        
        if success:
            flash("تمت المزامنة وتحديث البيانات بنجاح", "success")
        else:
            flash("فشلت عملية المزامنة. يرجى مراجعة سجلات النظام (Logs) لمعرفة السبب.", "danger")
            
    except Exception as e:
        # عرض الخطأ التقني بالتفصيل للمطور
        error_details = str(e)
        flash(f"حدث خطأ تقني غير متوقع: {error_details}", "danger")
        # طباعة تفاصيل الخطأ في الـ Logs الخاصة بـ Render للرجوع إليها
        traceback.print_exc()
        
    return redirect(url_for('orders.dashboard'))

@orders_bp.route('/view-order/<string:order_id>') 
@login_required
def view_order(order_id):
    """عرض تفاصيل طلب محدد."""
    result = db.session.query(Order, OrderFinancial)\
        .filter(Order.id == order_id)\
        .join(OrderFinancial, Order.id == OrderFinancial.order_id).first_or_404()
        
    return render_template('admin/order_details.html', order=result[0], financial=result[1])
