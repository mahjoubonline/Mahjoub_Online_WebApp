from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user
from core.models.user import User

def handle_admin_login():
    """منطق التحقق المركزي لسيادة القائد"""
    # إذا كان القائد مسجلاً بالفعل، يتم توجيهه للوحة التحكم فوراً
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. البحث عن المستخدم في الترسانة الرقمية
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # حالة: المستخدم غير موجود نهائياً
            flash("⚠️ عذراً، هذا المستخدم غير مسجل في النظام.")
            return render_template('login.html')
        
        # 2. التحقق من كلمة المرور
        if not user.check_password(password):
            # حالة: اسم المستخدم صح لكن كلمة المرور خطأ
            flash("❌ كلمة المرور غير صحيحة، حاول مجدداً.")
            return render_template('login.html')
        
        # 3. التحقق من الصلاحيات (الرتبة السيادية)
        if user.role != 'admin':
            flash("🚫 الوصول مرفوض: الحساب لا يملك صلاحيات إدارية.")
            return render_template('login.html')

        # 4. التحقق من حالة الحساب
        if not user.is_active_account:
            flash("🔒 الحساب موقوف حالياً، يرجى مراجعة الدعم الفني.")
            return render_template('login.html')
            
        # إذا اجتاز كل الاختبارات بنجاح
        login_user(user)
        return redirect(url_for('admin.admin_dashboard'))
            
    # العرض الأولي للبوابة (GET request)
    return render_template('login.html')
