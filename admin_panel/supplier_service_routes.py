# admin_panel/supplier_service_routes.py
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from admin_panel import admin_bp
from core import db
from core.models.supplier import Supplier, SupplierStaff

@admin_bp.route('/suppliers/profile/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def supplier_profile(supplier_id):
    """
    مسار إدارة بروفايل المورد السيادي:
    - GET: عرض بيانات المورد وطاقم العمل.
    - POST (AJAX): تحديث الحقول بشكل فردي (الحفظ التلقائي).
    - POST (Form): إضافة موظفين جدد لطاقم العمل.
    """
    supplier = Supplier.query.get_or_404(supplier_id)

    # 1. بروتوكول التحديث القادم من AJAX (الحفظ التلقائي للحقول)
    if request.method == 'POST' and request.is_json:
        try:
            data = request.get_json()
            field = data.get('field')
            value = data.get('value')
            
            # التأكد من وجود الحقل في كائن المورد
            if hasattr(supplier, field):
                setattr(supplier, field, value)
                db.session.commit()
                return jsonify({
                    "status": "success", 
                    "message": "تم تعميد التحديث بنجاح في قاعدة البيانات."
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": f"الحقل '{field}' غير موجود في نظام الموردين."
                }), 400
                
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "status": "error", 
                "message": f"حدث خطأ في محرك التحديث: {str(e)}"
            }), 500

    # 2. بروتوكول إضافة موظف جديد (من نافذة المودال)
    if request.method == 'POST' and 'new_username' in request.form:
        try:
            username = request.form.get('new_username')
            name = request.form.get('full_name')
            password = request.form.get('new_password')
            
            # إنشاء عضو جديد في طاقم العمل
            new_staff = SupplierStaff(
                supplier_id=supplier_id,
                username=username,
                name=name
            )
            new_staff.set_password(password)
            
            db.session.add(new_staff)
            db.session.commit()
            flash(f"✅ تم إضافة الموظف {name} إلى طاقم العمل بنجاح.", "success")
            
        except Exception as e:
            db.session.rollback()
            flash(f"⚠️ تعذر إضافة الموظف: {str(e)}", "danger")
            
        return redirect(url_for('admin.supplier_profile', supplier_id=supplier_id))

    # 3. بروتوكول العرض (GET)
    return render_template(
        'suppliers/supplier_profile.html', 
        supplier=supplier
    )

"""
--- ملاحظات القيادة التقنية ---
1. تم دمج DB Session مباشرة لضمان سرعة الحفظ دون الاعتماد على خدمات خارجية معطلة.
2. المسار يدعم استقبال JSON لخدمة وظائف الـ JavaScript التي برمجناها في القالب.
3. النظام الآن يربط تلقائياً بين واجهة "حوكمة البيانات" وقاعدة بيانات Postgres.
"""
