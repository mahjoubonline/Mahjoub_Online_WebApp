from flask import render_template, request, redirect, url_for, flash
# استيراد db من المجلد الأساسي core بناءً على هيكلية مشروعك
from core import db 

# تصحيح مسار الاستيراد: النماذج موجودة داخل core
# بناءً على سطر (from core.models.user import User) في ملفك السابق
from core.models.user import User
# يجب أن يكون استيراد طلبات السحب من نفس المسار
try:
    from core.models.finance import WithdrawRequest 
except ImportError:
    # إذا كان الملف موجوداً في مجلد models مباشرة داخل core
    from core.models import WithdrawRequest

# استيراد البلوبرنت الخاص بالإدارة المعرف في نفس المجلد
from . import admin_bp

@admin_bp.route('/withdraw-requests')
def withdraw_requests():
    """
    عرض كافة طلبات تصفية الأرصدة المعلقة للموردين.
    يتم جلب البيانات حية من قاعدة البيانات لضمان الدقة المالية.
    """
    try:
        # جلب الطلبات المعلقة وترتيبها من الأحدث
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """
    دالة التعميد المالي: تؤرشف بيانات التحويل وتحدث الحالة في قاعدة البيانات.
    """
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    if not request_id or not reference_number:
        flash("تنبيه: يجب إدخال رقم الحوالة المرجعي لإتمام العملية.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    # البحث عن الطلب
    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if not withdrawal_entry:
        flash("خطأ: لم يتم العثور على السجل.", "danger")
        return redirect(url_for('admin.withdraw_requests'))

    try:
        # تحديث بيانات التعميد
        withdrawal_entry.status = 'completed'
        withdrawal_entry.bank_used = bank_name
        withdrawal_entry.reference_id = reference_number
        
        # حفظ التغييرات سيادياً في قاعدة البيانات
        db.session.commit()
        
        flash(f"تم تعميد الحوالة رقم ({reference_number}) بنجاح وأرشفة الطلب.", "success")
        
    except Exception as e:
        db.session.rollback() # التراجع لضمان سلامة الأرصدة
        flash(f"فشل نظام الأرشفة: {str(e)}", "danger")

    return redirect(url_for('admin.withdraw_requests'))
