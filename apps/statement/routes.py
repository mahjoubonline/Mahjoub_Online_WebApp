# coding: utf-8
# 📂 apps/statement/routes.py - معالج التقارير المالي

from flask import render_template, make_response, abort
from flask_login import login_required, current_user
from . import statement_blueprint  # استيراد الـ Blueprint من نفس المجلد
from apps.models.statement_db import SupplierStatement

@statement_blueprint.route('/api/statement/report/pdf', methods=['GET'])
@login_required
def export_report_pdf():
    # 🛡️ الحماية: السماح فقط للأدمن أو صاحب الحساب بالوصول
    if current_user.role not in ['Owner', 'Admin']:
        abort(403)

    # استيراد ذكي (Lazy Import) لمنع تعطل التطبيق إذا لم تُثبت المكتبة
    try:
        from weasyprint import HTML
    except ImportError:
        return "❌ خطأ فني: مكتبة توليد ملفات PDF غير متوفرة.", 500

    try:
        # 1. جلب البيانات
        data = SupplierStatement.query.all() 
        
        # 2. تجهيز الـ HTML (تأكد أن القالب موجود في templates/pdf_template.html)
        rendered = render_template('pdf_template.html', report_data=data)
        
        # 3. تحويل HTML إلى PDF
        pdf = HTML(string=rendered).write_pdf()
        
        # 4. إعداد الرد الأمني
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=sovereign_statement.pdf'
        
        return response
        
    except Exception as e:
        # تسجيل الخطأ في السيرفر دون كشف تفاصيل حساسة للمستخدم
        print(f"🚨 خطأ في توليد PDF: {e}")
        return "❌ حدث خطأ أثناء معالجة التقرير المالي.", 500
