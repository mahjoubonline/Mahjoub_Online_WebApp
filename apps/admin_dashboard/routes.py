# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - لوحة التحكم السيادية (مُحَصّنة ومستقرة)

from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from apps.extensions import db
from sqlalchemy import func
from datetime import datetime

# استيراد النماذج الموجودة فعلياً
from apps.models.supplier_db import Supplier

admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.before_request
@login_required
def make_session_permanent():
    session.permanent = True
    session.modified = True 

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # 🛡️ حماية سيادية
    if current_user.role not in ['Owner', 'Admin']:
        abort(403)

    try:
        # إحصائيات الموردين
        total_suppliers = Supplier.query.count()
        
        # ملاحظة: تم إيقاف استدعاءات المحفظة مؤقتاً لحين إعادة بناء الجداول.
        # سيتم تفعيلها فور الانتهاء من كتابة أكواد الـ Models الجديدة.
        
        context = {
            'total_suppliers': total_suppliers,
            # 'total_balance_sar' و 'recent_transactions' سيتم إضافتها لاحقاً
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': current_user.username,
            'store_name': 'محجوب أونلاين'
        }
        
        return render_template('admin/dashboard_content.html', **context)
        
    except Exception as e:
        return f"🚨 خطأ تقني: {str(e)}", 500

@admin_dashboard.route('/system_logs', methods=['GET'])
@login_required
def system_logs():
    if current_user.role != 'Owner':
        abort(403)
    return "سجل الأحداث السيادي - قيد التطوير"
