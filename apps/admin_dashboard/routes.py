# coding: utf-8
# 📂 apps/admin_dashboard/routes.py

from flask import Blueprint, render_template
from flask_login import login_required

# تعريف البلوبرينت الخاص بالإدارة
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

# لاحظ هنا: نستخدم مسارات تبدأ بدون '/' في البداية أو بـ '/' 
# ولكن بعد إضافة الـ url_prefix='/admin' في الـ registry، 
# أي مسار هنا سيصبح تلقائياً تحت /admin/
@admin_dashboard.route('/dashboard') # سيصبح الرابط: /admin/dashboard
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_dashboard.route('/settings') # سيصبح الرابط: /admin/settings
@login_required
def settings():
    return render_template('admin/settings.html')
