# coding: utf-8
# 📂 apps/orders/routes.py - نسخة كاشفة للأخطاء (Debug-Ready)

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from apps.models.orders_db import ProcessedOrder, db
from apps.api.sync_engine import SyncEngine
import logging

orders_blueprint = Blueprint('orders', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

@orders_blueprint.route('/dashboard', methods=['GET'])
@login_required
def orders_dashboard():
    orders = ProcessedOrder.query.order_by(ProcessedOrder.created_at_api.desc()).all()
    return render_template('admin/orders_dashboard.html', orders=orders)

@orders_blueprint.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """مزامنة شاملة مع كشف الأخطاء الحقيقي"""
    try:
        # التعديل: المحرك الآن يرجع (success, message) بدلاً من Boolean فقط
        # ملاحظة: إذا لم نعدل المحرك، سأفترض أننا نكتفي بالتسجيل في الـ Logs
        success = SyncEngine.fetch_and_sync_order()
        
        if success:
            flash("✅ تمت المزامنة بنجاح.", "success")
        else:
            # هنا التعديل: سنظهر رسالة توجيهية للمستخدم
            flash("⚠️ فشلت المزامنة. راجع 'Logs' في Render لمعرفة السبب التقني (قد يكون التوكن أو اسم الاستعلام).", "danger")
            
    except Exception as e:
        logger.error(f"❌ [Routes] خطأ غير متوقع في مسار المزامنة: {e}")
        flash(f"خطأ غير متوقع: {str(e)}", "danger")
        
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/cancel/<order_id>', methods=['POST'])
@login_required
def cancel_order_route(order_id):
    result = SyncEngine.cancel_order(order_id)
    if result and 'errors' not in result:
        flash(f"تم إلغاء الطلب {order_id}.", "info")
    else:
        error_msg = result.get('errors', 'خطأ غير معروف') if result else "تعذر الاتصال بـ API"
        flash(f"فشل الإلغاء: {error_msg}", "danger")
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/fulfill/<order_id>', methods=['POST'])
@login_required
def fulfill_order_route(order_id):
    result = SyncEngine.mark_as_fulfilled(order_id)
    if result and 'errors' not in result:
        flash(f"تم تحديث الطلب {order_id} ليكون مشحوناً.", "success")
    else:
        flash("فشل تحديث حالة الشحن في قمرة.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/process/<order_id>', methods=['POST'])
@login_required
def process_order(order_id):
    order = ProcessedOrder.query.get(order_id)
    if not order:
        flash("الطلب غير موجود محلياً.", "danger")
        return redirect(url_for('orders.orders_dashboard'))
    
    try:
        order.status = 'settled'
        db.session.commit()
        flash(f"تمت التسوية المالية للطلب {order_id}.", "success")
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ [Financial Error] {order_id}: {e}")
        flash("خطأ أثناء التسوية المالية.", "danger")
        
    return redirect(url_for('orders.orders_dashboard'))

@orders_blueprint.route('/update-status/<order_id>', methods=['POST'])
@login_required
def update_status_route(order_id):
    new_status = request.form.get('status')
    if not new_status:
        flash("يرجى اختيار حالة صالحة.", "warning")
        return redirect(url_for('orders.orders_dashboard'))
        
    result = SyncEngine.update_order_status(order_id, new_status)
    if result and 'errors' not in result:
        flash(f"تم تحديث الحالة للطلب {order_id}.", "success")
    else:
        flash("فشل التحديث في قمرة.", "danger")
    return redirect(url_for('orders.orders_dashboard'))
