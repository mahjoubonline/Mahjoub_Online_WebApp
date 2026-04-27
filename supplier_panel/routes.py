from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials

@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and session.get('user_type') == 'supplier':
        return redirect(url_for('supplier_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        message, category, user = verify_supplier_credentials(username, password)
        
        if user and user.role == 'supplier': 
            session.permanent = True
            session['user_type'] = 'supplier' 
            login_user(user)
            flash(f'مرحباً بك في منصة محجوب أونلاين.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message or "بيانات غير صحيحة.", 'danger')
            
    return render_template('supplier_panel/login.html')
