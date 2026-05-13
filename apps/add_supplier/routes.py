import os
from flask import render_template, request, jsonify, url_for, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# الاستيراد المباشر لأن models في جذر المشروع
from models.admin_db import db, User, Supplier
# استدعاء البلوبرينت المعرف في __init__.py الخاص بالمجلد الحالي
from . import admin_suppliers

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    # ... باقي الكود الخاص بـ POST و GET كما هو دون تغيير ...
    # حساب المعرف القادم
    next_id = Supplier.query.count() + 1
    return render_template('admin/add_supplier.html', next_id=next_id)
