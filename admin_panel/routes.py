from flask import render_template, redirect, url_for
from flask_login import login_required, logout_user
from . import admin_bp
from .auth import handle_admin_login

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    return handle_admin_login()

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))
