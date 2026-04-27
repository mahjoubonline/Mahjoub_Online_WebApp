from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required 
from core import db
from core.models import Product, Supplier, User 
# تأكد من وجود ملف qumra_connector أو قم بتعطيل السطر التالي مؤقتاً إذا سبب خطأ
# from core.qumra_connector import QumraConnector 

@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if session.get('user_type') == 'supplier':
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            logout_user()
            session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى إدخال بيانات الهوية السيادية للمورد.', 'warning')
            # تأكد أن اسم الملف هنا login.html وليس supplier_login.html
            return render_template('supplier_panel/login.html')

        message, category, user = verify_supplier_credentials(username, password)
        
        if user and user.role == 'supplier': 
            session.permanent = True
            session['user_type'] = 'supplier' 
            login_user(user)
            
            supplier_name = user.supplier_profile.trade_name if user.supplier_profile else user.username
            flash(f'مرحباً بك يا {supplier_name} في منصة محجوب أونلاين.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message or "عذراً، هذه البوابة للموردين فقط.", 'danger')
            
    # العودة للقالب (يجب أن يكون اسمه login.html)
    return render_template('supplier_panel/login.html')
