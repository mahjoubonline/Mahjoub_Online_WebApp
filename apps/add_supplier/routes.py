from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from models.supplier_db import db, Supplier  
from datetime import datetime
from functools import wraps

# البلوبرنت الخاص بإدارة الموردين
admin_suppliers = Blueprint('admin_suppliers', __name__, template_folder='templates')

# 🛡️ بوابة التحقق السيادية
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('تنبيه: يجب تسجيل الدخول للوصول إلى أنظمة الموردين.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_suppliers.route('/add-supplier', methods=['GET', 'POST'])
@login_required  # تأمين المسار
def add_supplier():
    if request.method == 'POST':
        supplier_name = request.form.get('supplier_name')
        region = request.form.get('region')  # عدن، الخوخة، المخاء
        contact_number = request.form.get('contact_number')
        category = request.form.get('category')

        if not supplier_name or not region:
            flash('يرجى إدخال البيانات الأساسية (الاسم والمنطقة).', 'warning')
            return redirect(url_for('admin_suppliers.add_supplier'))

        try:
            new_supplier = Supplier(
                name=supplier_name,
                region=region,
                contact=contact_number,
                category=category,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_supplier)
            db.session.commit()
            
            flash(f'تم تعميد المورد "{supplier_name}" بنجاح في قطاع {region}.', 'success')
            return redirect(url_for('admin.dashboard')) # العودة لمركز المراقبة بعد النجاح

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ تقني في قاعدة البيانات: {str(e)}', 'danger')

    # 💡 التعديل الجوهري: تحديد المسار الصحيح داخل مجلد admin
    return render_template('admin/add_supplier.html')

@admin_suppliers.route('/api/suppliers-stats')
@login_required
def suppliers_stats():
    """واجهة برمجية لجلب إحصائيات الموردين لمركز المراقبة والتحكم"""
    try:
        count = Supplier.query.count()
        return jsonify({
            "status": "success",
            "total_suppliers": count,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
