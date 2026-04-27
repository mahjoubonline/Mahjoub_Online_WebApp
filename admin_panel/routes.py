from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from core import db
from core.models import User, Supplier, Product
from . import admin_bp 

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and session.get('user_type') == 'admin':
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()

        if user and check_password_hash(user.password, password):
            session.clear() 
            session['user_type'] = 'admin'
            login_user(user)
            flash('أهلاً بك أيها القائد علي في برج الرقابة.', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('الوصول للمنطقة السيادية مرفوض.', 'danger')
            
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if session.get('user_type') != 'admin':
        logout_user()
        return redirect(url_for('admin_panel.login'))
    return render_template('admin_panel/dashboard.html')
