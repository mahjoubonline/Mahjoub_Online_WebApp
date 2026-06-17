# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from apps.models.orders_db import ProcessedOrder
from apps.extensions import db
import logging

orders_blueprint = Blueprint('orders', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

@orders_blueprint.route('/dashboard', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض الطلبات مع معالجة دقيقة للأخطاء"""
    try:
        # جلب الطلبات مرتبة من الأحدث للأقدم
        orders = ProcessedOrder.query.order_by(ProcessedOrder.id.desc()).all()
        return render_template('admin/orders_dashboard.html', orders=orders)
    except Exception as e:
        logger.error(f"❌ خطأ فادح في لوحة الطلبات: {e}")
        flash("تعذر تحميل الطلبات، يرجى التحقق من قاعدة البيانات.", "danger")
        return render_template('admin/orders_dashboard.html', orders=[])

@orders_blueprint.route('/process/<order_id>', methods=['POST'])
@login_required
def process_order(order_id):
    """منطق تسوية الطلب مع حماية من الأخطاء"""
    try:
        order = ProcessedOrder.query.get(order_id)
        if order:
            order.status = 'settled'
            db.session.commit()
            flash(f"تمت تسوية الطلب {order_id} بنجاح.", "success")
        else:
            flash(f"الطلب {order_id} غير موجود في السجلات.", "warning")
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ خطأ أثناء تسوية الطلب {order_id}: {e}")
        flash("حدث خطأ تقني أثناء محاولة تسوية الطلب.", "danger")
    
    return redirect(url_for('orders.orders_dashboard'))
