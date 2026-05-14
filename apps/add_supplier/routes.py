from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import random
import string
from .models import db, Supplier  # استيراد الموديل وقاعدة البيانات

admin_suppliers = Blueprint('admin_suppliers', __name__)

def generate_temp_password(length=8):
    """توليد كلمة مرور مؤقتة للموردين الجدد"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استلام البيانات من النموذج (Frontend)
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            province = request.form.get('province')
            district = request.form.get('district')
            
            # تصحيح: استخدام address_detail ليطابق الهيكل البرمجي المطلوب
            address_detail = request.form.get('address_detail')
            
            # معالجة التصنيف (الفئة)
            category = request.form.get('category')
            if category == 'manual':
                category = request.form.get('manual_category')

            # معالجة الربط المالي
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            if bank_name == 'manual':
                bank_name = request.form.get('manual_bank_name')
            bank_acc = request.form.get('bank_acc')

            # 2. إنشاء سجل المورد الجديد في قاعدة البيانات
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=password, 
                category=category,
                owner_name=owner_name,
                trade_name=trade_name,
                phone=shop_phone,
                province=province,
                district=district,
                address_detail=address_detail,
                finance_type=fin_type,
                bank_name=bank_name,
                bank_account=bank_acc,
                created_at=datetime.utcnow()
            )

            db.session.add(new_supplier)
            db.session.commit()

            # 3. إرسال استجابة النجاح مع كافة البيانات المطلوبة للنسخ
            return jsonify({
                'status': 'success',
                'message': 'تم تعميد المورد بنجاح في نظام محجوب أونلاين',
                'data': {
                    'trade_name': trade_name,
                    'owner_name': owner_name,
                    'sovereign_id': unified_id,
                    'username': username,
                    'password': password,
                    'note': 'يرجى تغيير كلمة المرور المؤقتة فور تسجيل الدخول حفاظاً على أمان الحساب'
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'حدث خطأ أثناء التعميد: {str(e)}'
            }), 400

    # في حالة GET: استخراج آخر ID لتوليد المعرف التسلسلي التالي
    last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id = (last_supplier.id + 1) if last_supplier else 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)
