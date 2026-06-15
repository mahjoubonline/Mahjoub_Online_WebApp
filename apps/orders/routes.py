# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.utils.orders_engine import OrdersEngine
import logging

# تعريف الـ Blueprint
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/dashboard', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض لوحة التحكم الخاصة بالطلبات المجلوبة من قمرة"""
    try:
        columns = [
            {'label': 'رقم الطلب', 'key': 'order_id_qumra'},
            {'label': 'العميل', 'key': 'customer_name'},
            {'label': 'الإجمالي', 'key': 'total'},
            {'label': 'الحالة', 'key': 'status'},
            {'label': 'التاريخ', 'key': 'created_at'}
        ]
        
        engine = OrdersEngine()
        # جلب الطلبات المحفوظة محلياً بعد مزامنتها من قمرة
        orders = engine.get_all_orders()
        
        return render_template(
            'admin/orders_dashboard.html', 
            orders=orders, 
            columns=columns
        )
    except Exception as e:
        logging.error(f"خطأ في عرض لوحة الطلبات: {str(e)}")
        return "حدث خطأ داخلي في النظام", 500

@orders_bp.route('/sync-orders', methods=['POST'])
@login_required
def sync_orders():
    """طلب مزامنة البيانات من قمرة إلى النظام المحلي"""
    try:
        engine = OrdersEngine()
        # هنا يتم الاتصال بـ API قمرة وجلب البيانات وتخزينها
        success = engine.sync_orders_from_source()
        return jsonify({'success': success, 'message': 'تمت المزامنة بنجاح'})
    except Exception as e:
        logging.error(f"خطأ أثناء مزامنة البيانات من قمرة: {str(e)}")
        return jsonify({'success': False, 'message': 'فشل الاتصال بمنصة قمرة'}), 500

@orders_bp.route('/update-order-status', methods=['POST'])
@login_required
def update_order_status():
    """تحديث الحالة محلياً"""
    try:
        data = request.get_json()
        engine = OrdersEngine()
        success = engine.update_status(data.get('orderId'), data.get('value'))
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False}), 500
