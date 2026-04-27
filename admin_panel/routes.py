from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin_bp
from core.models import User, Supplier, Product

@admin_bp.route('/login')
def login():
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_panel/dashboard.html')

@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    # صفحة إدارة الموردين
    return render_template('admin_panel/admin_suppliers_management.html')

@admin_bp.route('/wallets')
@login_required
def wallets():
    return render_template('admin_panel/wallets.html')
