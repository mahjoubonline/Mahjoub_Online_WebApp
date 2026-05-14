from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import random
import string
from .models import db, Supplier  # تأكد من مسار الاستيراد الصحيح للموديل الخاص بك

admin_suppliers = Blueprint('admin_suppliers', __name__)

def generate_temp_password(length=8):
    """توليد كلمة مرور مؤقتة للموردين الجدد"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # استخراج البيانات من النموذج المرسل
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            category = request.form.get('category')
            
            # معالجة الفئة اليدوية إذا وجدت
            if category == 'manual':
                category = request.form.get('manual_category')

            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            province = request.form.get('province')
            district = request.form.get('district')
            
            # تم استخدام address_detail بناءً على هيكلية قاعدة البيانات وتصحيح الخطأ السابق
            address_detail = request.form.get('address_detail')
            
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            
            # معالجة البنك اليدوي
            if bank_name == 'manual':
                bank_name = request.form.get('manual_bank_name')
                
            bank_acc = request.form.get('bank_acc')

            # إنشاء كائن المورد الجديد
            new_supplier = Supplier(
                sovereign_id=unified_id, # المعرف الموحد السيادي
                username=username,
                password=password, # ملاحظة: يفضل تشفيرها في بيئة الإنتاج
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

            # إرسال استجابة النجاح شاملة كافة البيانات المطلوبة للعرض والنسخ
            return jsonify({
                'status': 'success',
                'message': 'تم تعميد المورد في النظام السيادي بنجاح',
                'data': {
                    'owner_name': owner_name,
                    'trade_name': trade_name,
                    'sovereign_id': unified_id,
                    'username': username,
                    'password': password,
                    'note': 'يرجى تغيير كلمة المرور المؤقتة فور الدخول الأول للحساب'
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'فشل في عملية التعميد: {str(e)}'
            }), 400

    # في حالة GET: حساب المعرف التالي للعرض في الصفحة
    last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id = (last_supplier.id + 1) if last_supplier else 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)
