from flask import render_template, redirect, url_for, flash, request
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # منطق التحقق من البيانات (اسم المستخدم وكلمة المرور)
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == "ali_admin" and password == "9046": # مثال
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('فشل التحقق السيادي: بيانات غير صحيحة', 'danger')
            
    # المسار المنظم للقالب كما طلبته
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
def admin_dashboard():
    return "مرحباً بك في لوحة تحكم محجوب أونلاين - برج الرقابة المركزية"
