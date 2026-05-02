from flask import render_template, request, redirect, url_for, flash
# استيراد db من المجلد الأساسي core بناءً على ملف __init__.py الخاص بك
from core import db 

# تصحيح الخطأ: ModuleNotFoundError: No module named 'models'
# بما أنك تستخدم بنية المجلدات الفرعية، يجب استيراد النماذج بمسارها الكامل
# إذا كان ملف النماذج داخل core/models/finance.py مثلاً، استخدم المسار الكامل
# سأفترض هنا أنها في المجلد الرئيسي لـ core أو فرعي منه:
try:
    from core.models.user import User  # استيراد المستخدم كما هو في __init__.py الخاص بك
    # استبدل السطر التالي بالمسار الحقيقي لملف WithdrawRequest لديك
    # مثال: من core.models.finance استورد WithdrawRequest
    from core.models.finance import WithdrawRequest 
except ImportError:
    # محاولة بديلة إذا كانت النماذج في مجلد فرعي آخر
    from models import WithdrawRequest 

# استيراد البلوبرنت الخاص بالإدارة
from . import admin_bp

@admin_bp.route('/withdraw-requests')
def withdraw_requests():
    """عرض كافة طلبات تصفية الأرصدة المعلقة للموردين"""
    try:
        # جلب الطلبات المعلقة وترتيبها من الأحدث
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات من النظام: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """دالة التعميد المالي لأرشفة بيانات التحويل وتصفية الأرصدة"""
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    if not request_id or not reference_number:
        flash("تنبيه: يجب إدخال رقم الحوالة المرجعي لإتمام عملية التعميد ياقائد.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if not withdrawal_entry:
        flash("خطأ: لم يتم العثور على سجل لهذا الطلب في النظام.", "danger")
        return redirect(url_for('admin.withdraw_requests'))

    try:
        # تحديث بيانات السجل المالي للتعميد والأرشفة
        withdrawal_entry.status = 'completed'
        withdrawal_entry.bank_used = bank_name
        withdrawal_entry.reference_id = reference_number
        
        # حفظ التغييرات نهائياً في قاعدة بيانات محجوب أونلاين
        db.session.commit()
        
        flash(f"تم تعميد الحوالة رقم ({reference_number}) بنجاح وأرشفة الطلب سيادياً.", "success")
        
    except Exception as e:
        db.session.rollback() # التراجع في حالة وجود خلل لضمان سلامة الأرصدة
        flash(f"فشل نظام الأرشفة في معالجة الطلب: {str(e)}", "danger")

    return redirect(url_for('admin.withdraw_requests'))
