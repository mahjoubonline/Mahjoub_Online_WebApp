from flask import render_template
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier
# استدعاء أي موديلات أخرى تحتاجها للحسابات
# from apps.models.order_db import Order 

@admin_dashboard.route('/admin/dashboard')
@login_required
def dashboard_home():
    # 1. جلب البيانات من القاعدة
    total_suppliers = Supplier.query.count()
    # يمكنك إضافة حساب الطلبات أو أي إحصائيات أخرى هنا
    active_orders = 0 
    
    # 2. تجهيز هيكل البيانات (stats)
    stats = {
        'total_suppliers': total_suppliers,
        'active_orders': active_orders,
        'system_health': '100%',
        'server_status': 'Online'
    }
    
    # 3. إرسال البيانات للقالب
    return render_template('admin/dashboard.html', 
                           owner=current_user, 
                           stats=stats)
