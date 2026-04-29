from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from core.models.user import User

admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin():
        return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_admin():
            login_user(user)
            return redirect(url_for('admin_panel.admin_dashboard'))
        flash('بيانات دخول المسؤول غير صحيحة.', 'danger')
    
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        return redirect(url_for('admin_panel.admin_login'))
    return render_template('admin_panel/dashboard.html')
