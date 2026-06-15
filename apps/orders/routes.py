# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.models.order_db import Order
from apps.extensions import db
from apps.utils.orders_engine import OrdersEngine
from flask_login import login_required
import logging

# إعداد الـ logger ليكون أكثر وضوحاً في Render
logger = logging.getLogger(__name__)

orders_bp = Blueprint('orders', __name__, template_folder='templates')
# 📂 apps/utils/orders_engine.py
from apps.extensions import db
from apps.models.order_db import Order
import requests
import logging

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        self.api_url = "https://mahjoub.online/admin/graphql"
        self.api_key = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        print("DEBUG: محاولة الاتصال بـ API قمرة - استعلام مصحح...")
        # الاستعلام المعدل ليتوافق مع هيكلية قمرة (status ككائن)
        payload = {
            "query": """
            query {
                findAllOrders(input: { limit: 50, page: 1 }) {
                    data {
                        _id
                        total
                        status {
                            value
                        }
                        customer {
                            name
                        }
                    }
                }
            }
            """
        }
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            result = response.json()
            
            # طباعة الرد للتأكد
            print(f"DEBUG: رد السيرفر بعد التصحيح: {result}")
            
            # استخراج البيانات
            orders = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            print(f"DEBUG: تم استخراج {len(orders)} طلب من البيانات.")
            return orders
        except Exception as e:
            print(f"DEBUG: خطأ في الاتصال: {str(e)}")
            return []

    def sync_orders_to_db(self):
        print("DEBUG: بدء عملية المزامنة...")
        orders = self.fetch_orders_from_qumra()
        
        count = 0
        for item in orders:
            order_id = str(item.get('_id'))
            if not order_id or order_id == "None": continue
            
            order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
            
            # تعبئة الأعمدة الأساسية
            order.total = float(item.get('total', 0))
            
            # معالجة الحالة ككائن (status { value })
            status_obj = item.get('status')
            if isinstance(status_obj, dict):
                order.status = str(status_obj.get('value', 'pending'))
            else:
                order.status = str(status_obj or 'pending')
            
            # تعبئة العميل
            if 'customer' in item and item['customer']:
                order.customer_name = item['customer'].get('name', 'غير معروف')
            
            # حفظ كامل البيانات الخام
            order.raw_data = item 
            
            db.session.add(order)
            count += 1
        
        db.session.commit()
        print(f"DEBUG: تمت المزامنة بنجاح، عدد الطلبات المضافة: {count}")
@orders_bp.route('/admin/orders', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض لوحة التحكم"""
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
    """المسار المسؤول عن المزامنة - تم تحسينه لكشف الأخطاء"""
    print("DEBUG: تم استدعاء مسار المزامنة /sync") # للتأكد من وصول الطلب
    try:
        engine = OrdersEngine()
        engine.sync_orders_to_db()
        return jsonify({'success': True, 'message': 'تمت المزامنة بنجاح.'})
    except Exception as e:
        # طباعة الخطأ في الـ Logs لتتمكن من رؤيته
        print(f"DEBUG: خطأ كارثي في المسار: {str(e)}")
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
            
        order.status = data.get('value')
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم التحديث'})
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: خطأ في التحديث: {str(e)}")
        return jsonify({'success': False, 'message': 'خطأ في التحديث'}), 500
