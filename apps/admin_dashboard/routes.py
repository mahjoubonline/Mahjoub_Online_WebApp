from flask import Blueprint, render_template, session, redirect, url_for
from models.supplier_db import Supplier # استيراد الموديل لعرض الإحصائيات

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/dashboard')
def dashboard():
    # 🛡️ بروتوكول الحماية: إذا لم يكن هناك ختم دخول، يتم الطرد فوراً للبوابة
    if not session.get('is_authenticated'):
        return redirect(url_for('auth.login'))
    
    # 📊 جلب إحصائيات سريعة لعرضها في "مركز المراقبة" (اختياري لكنه يعطي هيبة للوحة)
    try:
        suppliers_count = Supplier.query.count()
    except:
        suppliers_count = 0

    # توجيه المؤسس إلى واجهة المحتوى المركزية مع البيانات
    return render_template(
        'admin/dashboard_content.html', 
        suppliers_count=suppliers_count,
        admin_name="علي محجوب"
    )
