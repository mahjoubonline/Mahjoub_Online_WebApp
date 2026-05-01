from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User 
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active_account:
                flash('الحساب معلق.', 'warning')
                return redirect(url_for('admin.admin_login'))
            
            login_user(user)
            return redirect_by_role(user)
        flash('خطأ في البيانات.', 'danger')
            
    return render_template('login.html')

def redirect_by_role(user):
    if user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    elif user.role == 'supplier':
        return redirect(url_for('supplier.dashboard'))
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('admin.admin_login'))
    return render_template('dashboard.html')
