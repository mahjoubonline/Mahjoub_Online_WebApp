# coding: utf-8
# 📂 apps/statement/routes.py

from flask import render_template, request, jsonify, make_response
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.supplier_db import Supplier
from apps.utils.report_generator import ReportGenerator  # استدعاء محرك التقارير المركزي
from sqlalchemy import or_
from datetime import datetime, timedelta

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    currencies = ['USD', 'YER', 'SAR'] 
    return render_template('admin/statement.html', currencies=currencies)


# 1. البحث الذكي المتوافق بالكامل مع متطلبات الـ Select2 في الواجهة
@statement_blueprint.route('/api/suppliers/search', methods=['GET'])
@login_required
def api_search_suppliers():
    term = request.args.get('q', '')
    if not term:
        return jsonify({"results": []})

    try:
        # تم تنظيف الفلتر من حقل 'store_name' لحل مشكلة الـ AttributeError نهائياً
        suppliers = Supplier.query.filter(or_(
            Supplier.trade_name.ilike(f'%{term}%'),
            Supplier.owner_name.ilike(f'%{term}%'),
            Supplier.sovereign_id.ilike(f'%{term}%')
        )).limit(15).all()
        
        # استخدام getattr لضمان عدم توقف النظام حتى لو غاب أحد الحقول برمجياً
        results = [
            {
                'id': s.id, 
                'text': f"{getattr(s, 'trade_name', '---')} (المالك: {getattr(s, 'owner_name', '---')}) - المعرف: {getattr(s, 'sovereign_id', '---')}"
            } for s in suppliers
        ]
        return jsonify({"results": results})

    except Exception as e:
        # طباعة الخطأ في سجلات Railway لمتابعة جودة الاستعلام والتحقق اللحظي
        print(f"❌ Error during supplier search: {str(e)}")
        return jsonify({"results": [], "error": "حدث خطأ داخلي أثناء استعلام قاعدة البيانات"}), 500


# 2. جلب كشف الحساب الشامل والتقارير المالي عبر استدعاء الـ ReportGenerator
@statement_blueprint.route('/api/statement/report', methods=['GET'])
@login_required
def api_get_report():
    s_id = request.args.get('id', 'ALL')  # جعل القيمة الافتراضية ALL لعرض الحسابات الشاملة
    curr = request.args.get('currency', 'ALL')
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    # تحويل نصوص التواريخ القادمة من daterangepicker إلى كائنات datetime متوافقة مع قاعدة البيانات
    start_date = None
    end_date = None
    
    try:
        if start_str and start_str.strip():
            start_date = datetime.strptime(start_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        else:
            start_date = datetime.utcnow() - timedelta(days=30) # افتراضي آخر 30 يوم لحماية الأداء
            
        if end_str and end_str.strip():
            end_date = datetime.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        else:
            end_date = datetime.utcnow()
    except ValueError:
        return jsonify({'error': 'صيغة التاريخ غير صحيحة'}), 400

    # أ. استخراج الحركات التفصيلية للمورد (أو كل الحسابات إذا كانت القيمة ALL) عبر المحرك المركزي
    statements = ReportGenerator.get_detailed_transactions(
        supplier_id=s_id, 
        currency=curr, 
        start_date=start_date, 
        end_date=end_date
    )

    # ب. حساب صافي أرباح المنصة المرتبطة بالمورد والمحفظة عبر المحرك المركزي
    total_profit = ReportGenerator.calculate_net_profit(
        currency=curr, 
        start_date=start_date, 
        end_date=end_date
    )

    # ج. تجميع وإرسال البيانات بصيغة JSON النهائية لتغذية جدول الواجهة الفورية
    return jsonify({
        'summary': {
            'total_debit': float(sum(s.debit for s in statements)) if statements else 0.0,
            'total_credit': float(sum(s.credit for s in statements)) if statements else 0.0,
            'net_balance': float(sum(s.credit for s in statements) - sum(s.debit for s in statements)) if statements else 0.0,
            'total_profit': float(total_profit)
        },
        'details': [{
            'date': s.created_at.strftime('%Y-%m-%d %H:%M') if s.created_at else '---',
            'desc': getattr(s, 'description', getattr(s, 'desc', '---')) or '---',
            'ref': getattr(s, 'reference_number', getattr(s, 'ref', '---')) or '---',
            'currency': getattr(s, 'currency', 'USD'),
            'debit': float(s.debit or 0),
            'credit': float(s.credit or 0),
            'balance': float(s.running_balance or 0)
        } for s in statements]
    })


# 3. مسار تصدير وطباعة التقرير المالي كملف PDF مخصص بالهوية البصرية للمنصة
@statement_blueprint.route('/api/statement/report/pdf', methods=['GET'])
@login_required
def export_report_pdf():
    """ توليد وتصدير كشف الحساب المالي كملف PDF احترافي أو طباعته فورا """
    s_id = request.args.get('supplier_id', 'ALL')
    curr = request.args.get('currency', 'ALL')
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')
    
    start_date = None
    end_date = None
    
    try:
        if start_str and start_str.strip() and start_str != 'undefined':
            start_date = datetime.strptime(start_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        else:
            start_date = datetime.utcnow() - timedelta(days=30)
            
        if end_str and end_str.strip() and end_str != 'undefined':
            end_date = datetime.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        else:
            end_date = datetime.utcnow()
    except ValueError:
        return "صيغة التواريخ الممررة غير صالحة برمجياً", 400
    
    # استخراج الحركات التفصيلية من المحرك المطور
    statements = ReportGenerator.get_detailed_transactions(
        supplier_id=s_id, 
        currency=curr, 
        start_date=start_date, 
        end_date=end_date
    )
    
    # حساب الإجماليات برمجياً لضمان الدقة الكاملة حتى لو كانت صفرية للحسابات الخالية من الحركات
    total_debit = sum(float(s.debit or 0) for s in statements) if statements else 0.0
    total_credit = sum(float(s.credit or 0) for s in statements) if statements else 0.0
    net_balance = total_credit - total_debit
    
    # تحديد مسمى الحساب المستخرج
    supplier_name = "جميع الموردين والشركاء (عرض شامل)"
    if s_id and s_id != 'ALL':
        supplier = Supplier.query.get(s_id)
        if supplier:
            supplier_name = getattr(supplier, 'trade_name', getattr(supplier, 'owner_name', 'مورد معتمد'))

    # رندرة القالب المتواجد داخل المسار الذي أنشأته للتو
    html_content = render_template(
        'pdf_template.html',
        statements=statements,
        supplier_name=supplier_name,
        currency=curr,
        start_date=start_date.strftime('%Y/%m/%d'),
        end_date=end_date.strftime('%Y/%m/%d'),
        total_debit=total_debit,
        total_credit=total_credit,
        net_balance=net_balance,
        generated_at=datetime.utcnow().strftime('%Y/%m/%d %H:%M')
    )
    
    # لإعطاء مرونة طباعة قصوى وتفادي مشاكل غياب الحزم الخارجية على سيرفرات الاستضافة، 
    # نقوم بإرجاع المستند كـ HTML مهيأ بأوامر الطباعة التلقائية للمتصفح عبر خيارات العرض المباشر.
    response = make_response(html_content)
    return response
