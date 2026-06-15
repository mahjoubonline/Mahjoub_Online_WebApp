# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
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
    """عرض لوحة التحكم مع دعم البيانات الديناميكية"""
    try:
        page = request.args.get('page', 1, type=int)
        pagination = Order.query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template(
            'admin/orders_dashboard.html', 
            orders=pagination.items, 
            pagination=pagination
        )
    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        return "حدث خطأ أثناء تحميل الطلبات", 500

@orders_bp.route('/admin/orders/sync', methods=['POST'])
@login_required
def sync_orders():
    """مزامنة الطلبات: الآن النظام يحفظ كل شيء في raw_data تلقائياً"""
    try:
        engine = OrdersEngine()
        engine.sync_orders_to_db()
        return jsonify({'success': True, 'message': 'تمت المزامنة بنجاح وحفظ البيانات الخام.'})
    except Exception as e:
        logger.error(f"Sync error: {str(e)}")
        return jsonify({'success': False, 'message': f'فشل المزامنة: {str(e)}'}), 500

@orders_bp.route('/admin/orders/update-status', methods=['POST'])
@login_required
def update_order_status():
    """تحديث حالة الطلب"""
    try:
        data = request.json
        order = Order.query.get(data.get('orderId'))
        if not order:
            return jsonify({'success': False, 'message': 'الطلب غير موجود'}), 404
            
        # تحديث الحالة بناءً على النوع
        status_type = data.get('type')
        if status_type == 'payment':
            order.payment_status = data.get('value')
        else:
            order.status = data.get('value')
            
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم التحديث'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'خطأ في التحديث'}), 500
