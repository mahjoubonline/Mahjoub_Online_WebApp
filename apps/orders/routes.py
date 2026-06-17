# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from apps.models.orders_db import ProcessedOrder
from apps.extensions import db

orders_blueprint = Blueprint('orders', __name__, template_folder='templates')

@orders_blueprint.route('/dashboard', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض الطلبات السيادية بعد فك تشفير قيمتها لحظياً"""
    try:
        # جلب الطلبات من قاعدة البيانات
        orders = ProcessedOrder.query.all()
        return render_template('admin/orders_dashboard.html', orders=orders)
    except Exception as e:
        flash(f"حدث خطأ أثناء تحميل الطلبات: {e}", "danger")
        return render_template('admin/orders_dashboard.html', orders=[])

@orders_blueprint.route('/process/<order_id>', methods=['POST'])
@login_required
def process_order(order_id):
    """منطق تسوية الطلب"""
    order = ProcessedOrder.query.get(order_id)
    if order:
        order.status = 'settled'
        db.session.commit()
        flash(f"تمت تسوية الطلب {order_id} بنجاح.", "success")
    else:
        flash("الطلب غير موجود.", "danger")
    return redirect(url_for('orders.orders_dashboard'))
