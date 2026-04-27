from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from . import supplier_bp
from core.models import User # تأكد من استيراد موديل المستخدم

@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المستخدم في قاعدة البيانات
        user = User.query.filter_by(username=username).first()
        
        # التحقق من صحة البيانات (بفرض أنك تستخدم التحقق من الباسورد)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash('⚠️ خطأ في هوية الشريك أو شفرة العبور')
            
    return render_template('supplier_panel/supplier_login.html')
