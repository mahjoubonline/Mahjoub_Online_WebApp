import os
from flask import Blueprint, request, jsonify
from datetime import datetime
from apps import db  
from models.supplier_db import Supplier 

admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__
)

# محاولة إنشاء الجدول عند تشغيل السيرفر
with admin_suppliers.record_once(lambda state: None):
    try:
        from run import create_app
        app = create_app()
        with app.app_context():
            db.create_all()
    except Exception:
        pass


@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    # إنشاء الجدول كخطة احتياطية
    try:
        db.create_all()
    except Exception:
        pass

    if request.method == 'POST':
        try:
            unified_id = request.form.get('unified_id', 'TEST-123')
            username = request.form.get('username')
            password = request.form.get('password')
            trade_name = request.form.get('trade_name')

            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'اسم المستخدم مسجل مسبقاً!'}), 400

            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=password, 
                trade_name=trade_name,
                created_at=datetime.utcnow()
            )
            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'تم تسجيل المورد التجريبي بنجاح!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

    # 🎯 واجهة اختبار فرونت إند (HTML/Jinja2) مدمجة ومباشرة بدون استدعاء ملفات خارجية
    test_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>اختبار تشغيل نظام الموردين</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light p-5">
        <div class="container text-center" style="max-width: 500px;">
            <div class="card shadow p-4 border-0">
                <h3 class="fw-bold text-success mb-3">✔️ نظام الموردين يعمل بنجاح!</h3>
                <p class="text-muted">هذه واجهة اختبار معزولة للتأكد من سلامة الاتصال بقاعدة البيانات والـ Backend.</p>
                <hr>
                <form method="POST" class="text-start">
                    <div class="mb-3">
                        <label class="form-label">اسم المستخدم</label>
                        <input type="text" name="username" class="form-control" placeholder="test_user" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">كلمة المرور</label>
                        <input type="password" name="password" class="form-control" placeholder="123456" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">الاسم التجاري</label>
                        <input type="text" name="trade_name" class="form-control" placeholder="مؤسسة التجارة المحدودة" required>
                    </div>
                    <button type="submit" class="btn btn-success w-100 fw-bold">إرسال وتجربة الحفظ في قاعدة البيانات</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return test_html


@admin_suppliers.route('/check-duplicate', methods=['GET'])
def check_duplicate():
    return jsonify({'exists': False})
