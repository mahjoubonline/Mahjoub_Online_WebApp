# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify, current_app
from apps.models.order_db import Order
from apps.extensions import db
from apps.utils.orders_engine import OrdersEngine
from flask_login import login_required
import logging

logger = logging.getLogger(__name__)

orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/admin/orders', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض لوحة التحكم الخاصة بالطلبات"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        pagination = Order.query.order_by(Order.created_at.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        orders = pagination.items
        
        return render_template(
            'admin/orders_dashboard.html', 
            orders=orders, 
            pagination=pagination
        )
    
    except Exception as e:
        logger.error(f"Error in orders_dashboard: {str(e)}")
        return "حدث خطأ أثناء تحميل الطلبات.", 500

@orders_bp.route('/admin/orders/sync', methods=['POST'])
@login_required
def sync_orders():
    """مزامنة الطلبات من قمرة إلى قاعدة البيانات المحلية"""
    try:
        engine = OrdersEngine()
        # نقوم بالاستدعاء مباشرة، Engine مهيأ الآن للتعامل مع findAllOrders
        engine.sync_orders_to_db()
        
        return jsonify({
            'success': True, 
            'message': 'تمت عملية المزامنة بنجاح.'
        })
    except Exception as e:
        # تسجيل الخطأ بوضوح في الـ Logs
        logger.error(f"Sync error: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'فشل الاتصال بمنصة قمرة: {str(e)}'
        }), 500

@orders_bp.route('/admin/orders/update-status', methods=['POST'])
@login_required
def update_order_status():
    """تحديث حالة الطلب"""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'بيانات غير صالحة'}), 400
            
        order_id = data.get('orderId')
        status_type = data.get('type')
        new_value = data.get('value')
        
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'الطلب غير موجود'}), 404
            
        if status_type == 'payment':
            order.payment_status = new_value
        elif status_type == 'shipping':
            order.status = new_value
            
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم التحديث بنجاح'})
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update status error: {str(e)}")
        return jsonify({'success': False, 'message': 'فشل تحديث الحالة'}), 500
