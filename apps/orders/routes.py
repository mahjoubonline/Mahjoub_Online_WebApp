# coding: utf-8
# 📂 apps/orders/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from apps.models.orders_db import Order  # تأكد من تطابق مسار الموديل لديك
from apps.orders.services import OrderService
from apps import db

# تعريف الـ Blueprint
# هذا الـ Blueprint سيتم تسجيله تلقائياً بواسطة الـ registry.py الخاص بك
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/dashboard')
@login_required
def dashboard():
    """
    عرض لوحة تحكم الطلبات مع الإحصائيات الحية
    """
    # 1. حساب الإحصائيات (Stats) من قاعدة البيانات مباشرة
    # نستخدم db.func.sum لحساب الإجمالي بدقة من قاعدة البيانات
    total_sales = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    
    stats = {
        'cancelled': Order.query.filter_by(order_status='cancelled').count(),
        'completed': Order.query.filter_by(order_status='completed').count(),
        'total_sales': total_sales
    }
    
    # 2. جلب قائمة الطلبات لعرضها في الجدول (مرتبة من الأحدث للأقدم)
    items = Order.query.order_by(Order.id.desc()).all()
    
    return render_template('admin/orders_dashboard.html', stats=stats, items=items)

@orders_bp.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """
    دالة تشغيل المزامنة اليدوية عند الضغط على زر "مزامنة البيانات"
    """
    # هنا يتم استدعاء "المصنع" أو المحرك الذي برمجناه
    # تأكد من تمرير مفتاح الـ API الصحيح ومعرف المورد
    success = OrderService.fetch_and_sync_orders(api_key="YOUR_API_KEY", supplier_id=1)
    
    if success:
        flash("تمت المزامنة وتحديث البيانات بنجاح", "success")
    else:
        flash("حدث خطأ أثناء المزامنة، يرجى مراجعة سجلات الخطأ", "danger")
        
    # العودة إلى لوحة التحكم لرؤية النتائج
    return redirect(url_for('orders.dashboard'))

@orders_bp.route('/view-order/<int:order_id>')
@login_required
def view_order(order_id):
    """عرض تفاصيل طلب محدد"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_details.html', order=order)
