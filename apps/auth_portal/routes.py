# coding: utf-8
# 🔑 بوابة النفاذ السيادية - منصة محجوب أونلاين 2026
# التوثيق: إدارة جلسات الدخول، التحقق من الهوية، وحوكمة الصلاحيات

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from apps import db 
from apps.models.admin_db import AdminUser 
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المالك مسجل دخوله بالفعل، نقله مباشرة للوحة التحكم
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. البحث عن الهوية الرقمية في المنظومة
        user = AdminUser.query.filter_by(username=username).first()
        
        # 2. منطق التحقق المتقدم
        if not user:
            # السيناريو: اسم المستخدم غير مسجل
            flash('عذراً، هذه الهوية الرقمية غير مسجلة في منظومة محجوب أونلاين.', 'danger')
        
        elif not check_password_hash(user.password_hash, password):
            # السيناريو: اسم المستخدم صح لكن كلمة المرور خطأ
            flash('مفتاح التشفير (كلمة المرور) غير صحيح. يرجى المحاولة مرة أخرى.', 'danger')
        
        elif user.role not in ['Owner', 'Admin']:
            # السيناريو: المستخدم مسجل لكنه لا يملك صلاحيات وصول سيادية
            flash('ليس لديك صلاحيات النفاذ لهذه المنطقة السيادية.', 'warning')
            
        else:
            # النجاح: تسجيل الدخول وتوجيه المالك للداشبورد
            login_user(user)
            
            # تحديث وقت آخر ظهور (اختياري لزيادة الأمان)
            from datetime import datetime
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'مرحباً بك يا سيد {user.full_name} في سوقك الذكي.', 'success')
            return redirect(url_for('admin_dashboard.index'))
    
    # عرض صفحة الدخول (التصميم الملكي)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """إغلاق جلسة النفاذ والعودة للبوابة الرئيسية"""
    logout_user()
    flash('تم تسجيل الخروج من المنطقة السيادية بنجاح.', 'info')
    return redirect(url_for('auth_bp.login'))
