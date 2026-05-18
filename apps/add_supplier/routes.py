# coding: utf-8
# 🔑 محرك حوكمة الموردين والربط المالي السيادي لعام 2026 - منصة محجوب أونلاين

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

# استيراد البلوبرينت وكائن قاعدة البيانات المركزي والنماذج النواة
from . import admin_suppliers
from apps import db
from apps.models.supplier_db import Supplier

@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@login_required
def add_supplier_page():
    """
    مسار تعميد الموردين وإنشاء المحافظ المالية تلقائياً عبر مصيدة الحوكمة (Event Listener)
    """
    if request.method == 'POST':
        try:
            # 1. استقبال الحقول والنوايا الحوكمية من الواجهة الأمامية
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            identity_type = request.form.get('identity_type', '').strip()
            identity_number = request.form.get('identity_number', '').strip()
            owner_name = request.form.get('owner_name', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            owner_phone = request.form.get('owner_phone', '').strip()
            shop_phone = request.form.get('shop_phone', '').strip()
            province = request.form.get('province', '').strip()
            district = request.form.get('district', '').strip()
            address_detail = request.form.get('address_detail', '').strip()
            fin_type = request.form.get('fin_type', '').strip()
            bank_name = request.form.get('bank_name', '').strip()
            bank_acc = request.form.get('bank_acc', '').strip()
            activity_type = request.form.get('activity_type', '').strip()

            # فحص المدخلات الحرجة لضمان سلامة النواة ومنع الحقول الفارغة
            if not username or not password or not owner_name or not identity_number or not bank_acc:
                return jsonify({"status": "error", "message": "تنبيه حوكمي: الحقول الأساسية للتسجيل والتوثيق مطلوبة."}), 400

            # 2. فحص التكرار لمنع تضارب المسارات في قاعدة البيانات
            exists = db.session.query(Supplier.id).filter_by(username=username).first()
            if exists:
                return jsonify({"status": "error", "message": "اسم المستخدم هذا مسجل مسبقاً في النظام."}), 400

            # 3. 👑 تشغيل المحرك المباشر لتوليد المعرف السيادي النقي
            last_supplier = db.session.query(Supplier).order_by(Supplier.id.desc()).first()
            if last_supplier and last_supplier.sovereign_id:
                try:
                    parts = last_supplier.sovereign_id.split('MAH963')
                    last_num = int(parts[-1])
                    next_num = last_num + 1
                except (ValueError, IndexError):
                    next_num = (last_supplier.id or 0) + 1
            else:
                next_num = 1

            sovereign_id = f"SUP-MAH963{next_num}"

            # 4. تشفير كلمة المرور وتشييد كائن المورد بالبيانات المتكاملة
            hashed_password = generate_password_hash(password)
            new_supplier = Supplier(
                sovereign_id=sovereign_id,  # حقن المعرف الحقيقي الفوري هنا لحل مشكلة قيد Null
                username=username,
                password_hash=hashed_password,
                identity_type=identity_type,
                identity_number=identity_number,
                owner_name=owner_name,
                trade_name=trade_name,
                owner_phone=owner_phone,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address_detail=address_detail,
                fin_type=fin_type,
                bank_name=bank_name,
                bank_acc=bank_acc,
                activity_type=activity_type,
                registration_source='لوحة التحكم',
                rank_grade='سيادي',          
                status='active',          
                created_by_id=current_user.id if hasattr(current_user, 'id') else None
            )

            db.session.add(new_supplier)
            
            # تثبيت الحفظ يطلق الـ Event Listener المالي تلقائياً لإنشاء المحفظة بالتوافق التام
            db.session.commit() 

            return jsonify({
                "status": "success",
                "message": f"تم تعميد المورد بنجاح بالمعرف السيادي ({sovereign_id}) وتوليد محفظته الموثقة تلقائياً.",
                "data": {
                    "username": username,
                    "sovereign_id": sovereign_id
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ خطأ حرج أثناء حفظ المورد في الـ Routes: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"بنية النظام ترفض الحفظ بسبب تعارض داخلي: {str(e)}"
            }), 500

    # 5. معالجة مرحلة العرض اللحظي (GET)
    backup_csrf_token = ""
    try:
        if 'csrf' in current_app.extensions:
            from flask_wtf.csrf import generate_csrf
            backup_csrf_token = generate_csrf()
    except Exception:
        pass

    return render_template(
        'admin/add_supplier.html', 
        owner=current_user, 
        backup_csrf=backup_csrf_token
    )


@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """
    محرك الاستعلام والتحقق المباشر من الواجهة لمنع تكرار البيانات الفريدة
    """
    check_type = request.args.get('type', '').strip()
    value = request.args.get('value', '').strip()

    if not check_type or not value:
        return jsonify({"exists": False}), 400

    exists = False
    try:
        if check_type == 'username':
            exists = db.session.query(Supplier.id).filter_by(username=value).first() is not None
        elif check_type == 'identity_number':
            exists = db.session.query(Supplier.id).filter_by(identity_number=value).first() is not None
        elif check_type == 'bank_acc':
            exists = db.session.query(Supplier.id).filter_by(bank_acc=value).first() is not None
        elif check_type == 'owner_phone':
            exists = db.session.query(Supplier.id).filter_by(owner_phone=value).first() is not None
        elif check_type == 'shop_phone':
            exists = db.session.query(Supplier.id).filter_by(shop_phone=value).first() is not None
        elif check_type == 'trade_name':
            exists = db.session.query(Supplier.id).filter_by(trade_name=value).first() is not None
        elif check_type == 'owner_name':
            exists = db.session.query(Supplier.id).filter_by(owner_name=value).first() is not None
    except Exception as e:
        current_app.logger.error(f"Error checking duplicate: {e}")
        return jsonify({"exists": False, "error": str(e)}), 500

    return jsonify({"exists": exists}), 200
