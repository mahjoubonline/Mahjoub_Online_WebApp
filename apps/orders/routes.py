# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.models.order_db import Order
from apps.extensions import db
from apps.utils.bridge_engine import QumraBridgeEngine
from flask_login import login_required
import logging

logger = logging.getLogger(__name__)
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/admin/orders', methods=['GET'])
@login_required
def orders_dashboard():
    page = request.args.get('page', 1, type=int)
    pagination = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/orders_dashboard.html', orders=pagination.items, pagination=pagination)

@orders_bp.route('/admin/orders/sync', methods=['POST'])
@login_required
def sync_orders():
    print("DEBUG: بدء عملية المزامنة التشخيصية...")
    try:
        engine = QumraBridgeEngine()
        orders = engine.fetch_latest_orders()
        
        # 🚨 DEBUG: كشف هيكلية البيانات الحقيقية
        print(f"DEBUG: عدد الطلبات المستلمة: {len(orders)}")
        if orders:
            print(f"DEBUG: هيكل البيانات للطلب الأول: {orders[0]}")
        else:
            print("DEBUG: المصفوفة فارغة! لا توجد طلبات.")

        count = 0
        for item in orders:
            # نحاول التقاط المعرف بأكثر من طريقة
            order_id = str(item.get('_id') or item.get('id') or '')
            if not order_id: continue
            
            order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
            
            # التقاط السعر والحالة والعميل بمرونة
            order.total = float(item.get('totalPrice') or item.get('total') or 0)
            
            status_data = item.get('status')
            order.status = status_data.get('name') if isinstance(status_data, dict) else str(status_data or 'pending')
            
            account_data = item.get('account')
            order.customer_name = account_data.get('name') if isinstance(account_data, dict) else str(account_data or 'غير معروف')
            
            db.session.add(order)
            count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'تمت المزامنة: تمت معالجة {count} طلب.'})
        
    except Exception as e:
        print(f"DEBUG: خطأ كارثي في المزامنة: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@orders_bp.route('/admin/orders/update-status', methods=['POST'])
@login_required
def update_order_status():
    data = request.json
    order = Order.query.get(data.get('orderId'))
    if order:
        order.status = data.get('value')
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404
