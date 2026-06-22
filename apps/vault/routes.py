# coding: utf-8
# 📂 apps/vault/routes.py - مسارات الخزينة المركزية (معطلة مؤقتاً)

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

vault_bp = Blueprint('vault_bp', __name__, template_folder='templates')

@vault_bp.route('/admin/vault', methods=['GET'])
@login_required
def vault_dashboard():
    # تم تعطيل الكود مؤقتاً بسبب حذف الموديل vault_db
    flash("نظام الخزينة قيد الصيانة حالياً.", "info")
    return "نظام الخزينة غير متاح حالياً", 503

@vault_bp.route('/admin/vault/verify', methods=['POST'])
@login_required
def verify_integrity():
    flash("نظام الخزينة غير متاح حالياً.", "error")
    return redirect(url_for('vault_bp.vault_dashboard'))
