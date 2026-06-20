# coding: utf-8
# 📂 apps/orders/routes.py - المحرك السيادي لمعالجة الطلبات (نسخة أداء عالٍ)

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps.extensions import db
from apps.models import ProcessedOrder
from apps.api.sync_engine import SyncEngine
from sqlalchemy import func
import logging

orders_bp = Blueprint('orders', __name__, url_prefix='/orders', template_folder='templates')
logger = logging.getLogger(__name__)

# 1. لوحة تحكم الطلبات (بأداء محسن عبر قاعدة البيانات)
@orders_bp.route('/dashboard')
def orders_dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    # تحسين الأداء: إجراء الحسابات في قاعدة البيانات مباشرة بدلاً من جلب كل السجلات
    stats = db.session.query(
        func.sum(ProcessedOrder.total_price).label('total_sales'),
        func.count(ProcessedOrder.id).filter(ProcessedOrder.order_status == 'delivered').label('completed'),
        func.count(ProcessedOrder.id).filter(ProcessedOrder.order_status == 'cancelled').label('cancelled')
    ).first()
    
    # بناء استعلام البحث
    query = ProcessedOrder.query.order_by(ProcessedOrder.id.desc())
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (ProcessedOrder.order_id.ilike(search_filter)) | 
            (ProcessedOrder.customer_name.ilike(search_filter))
        )
    
    # التقسيم (Pagination) الاحترافي
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/orders_dashboard.html', 
                           items=pagination.items,
                           total_pages=pagination.pages,
                           current_page=page,
                           stats={
                               'total_sales': stats.total_sales or 0, 
                               'completed': stats.completed or 0, 
                               'cancelled': stats.cancelled or 0
                           }, 
                           search=search)

# 2. المزامنة
@orders_bp.route('/sync-all', methods=['POST'])
def sync_all():
    if SyncEngine.fetch_and_sync_order():
        flash("✅ تمت المزامنة بنجاح!", "success")
    else:
        flash("⚠️ فشلت المزامنة، يرجى مراجعة سجلات الأخطاء.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

# 3. تحديث الحقول لحظياً (AJAX)
@orders_bp.route('/update-order-field/<order_id>', methods=['POST'])
def update_order_field(order_id):
    data = request.json
    order = ProcessedOrder.query.get(order_id)
    if order and hasattr(order, data.get('field')):
        try:
            setattr(order, data['field'], data['value'])
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            logger.error(f"Error updating field: {e}")
            return jsonify({'status': 'error', 'message': 'فشل تحديث البيانات'}), 500
    return jsonify({'status': 'error', 'message': 'الطلب غير موجود أو الحقل غير مسموح'}), 404

# 4. حذف طلب
@orders_bp.route('/delete-order/<order_id>', methods=['POST'])
def delete_order(order_id):
    order = ProcessedOrder.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'الطلب غير موجود'}), 404
