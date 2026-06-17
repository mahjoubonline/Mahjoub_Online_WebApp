# coding: utf-8
# 📂 apps/orders/routes.py - لوحة تحكم الطلبات والعمليات (النسخة النهائية المتكاملة)

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from apps.models.orders_db import ProcessedOrder
from apps.api.sync_engine import SyncEngine
from apps.extensions import db
import logging

orders_blueprint = Blueprint('orders', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

@orders_blueprint.route('/dashboard', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض لوحة التحكم مع جلب الطلبات من قاعدة البيانات المحلية"""
    # ترتيب حسب تاريخ الإنشاء من API قمرة
    orders = ProcessedOrder.query.order_by(ProcessedOrder.created_at_api.desc()).all()
    return render_template('admin/orders_dashboard.html', orders=orders)

@orders_blueprint.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """مزامنة شاملة لجميع الطلبات من قمرة"""
    if SyncEngine.fetch_and_sync_order():
        flash("تمت مزامنة جميع الطلبات بنجاح من قمرا.", "success")
    else:
        flash("فشلت المزامنة، يرجى التحقق من اتصال API في السجلات.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/cancel/<order_id>', methods=['POST'])
@login_required
def cancel_order_route(order_id):
    """إلغاء الطلب في قمرة ومحلياً"""
    result = SyncEngine.cancel_order(order_id)
    if result:
        flash(f"تم إرسال طلب إلغاء الطلب {order_id} بنجاح.", "info")
    else:
        flash(f"فشل الاتصال بـ قمرة لإلغاء الطلب {order_id}.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/fulfill/<order_id>', methods=['POST'])
@login_required
def fulfill_order_route(order_id):
    """تعليم الطلب كمشحون في قمرة"""
    result = SyncEngine.mark_as_fulfilled(order_id)
    if result:
        flash(f"تم تحديث حالة الطلب {order_id} كـ مشحون.", "success")
    else:
        flash(f"فشل تحديث حالة الشحن في قمرة.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/update-status/<order_id>', methods=['POST'])
@login_required
def update_status_route(order_id):
    """تحديث حالة الطلب يدوياً"""
    new_status = request.form.get('status')
    if not new_status:
        flash("الحالة المطلوبة غير صالحة.", "warning")
        return redirect(url_for('orders.orders_dashboard'))
        
    result = SyncEngine.update_order_status(order_id, new_status)
    if result:
        flash(f"تم تحديث حالة الطلب {order_id} إلى {new_status}.", "success")
    else:
        flash("خطأ في تحديث الحالة.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/process/<order_id>', methods=['POST'])
@login_required
def process_order(order_id):
    """تسوية مالية محلية (Internal Settlement)"""
    order = ProcessedOrder.query.get(order_id)
    if not order:
        flash("الطلب غير موجود في النظام.", "danger")
        return redirect(url_for('orders.orders_dashboard'))
    
    try:
        order.status = 'settled'
        db.session.commit()
        flash(f"تمت التسوية المالية للطلب {order_id} بنجاح.", "success")
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ [Financial Settlement Error] Order ID {order_id}: {e}")
        flash("حدث خطأ تقني أثناء التسوية المالية.", "danger")
        
    return redirect(url_for('orders.orders_dashboard'))
