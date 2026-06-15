# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.models.order_db import Order
from apps.extensions import db

orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/admin/orders', methods=['GET'])
def orders_dashboard():
    # الحصول على رقم الصفحة من الرابط (مثلاً ?page=1)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # جلب الطلبات مع الترقيم، وترتيبها من الأحدث للأقدم
    pagination = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page)
    orders = pagination.items
    
    return render_template('admin/orders_dashboard.html', 
                           orders=orders, 
                           pagination=pagination)

@orders_bp.route('/admin/orders/update-status', methods=['POST'])
def update_order_status():
    """دالة لتحديث حالة الطلب عبر AJAX"""
    data = request.json
    order_id = data.get('orderId')
    status_type = data.get('type') # 'payment' أو 'shipping'
    new_value = data.get('value')
    
    order = Order.query.get(order_id)
    if order:
        if status_type == 'payment':
            order.payment_status = new_value
        elif status_type == 'shipping':
            order.status = new_value
            
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم التحديث بنجاح'})
    
    return jsonify({'success': False, 'message': 'الطلب غير موجود'}), 404
