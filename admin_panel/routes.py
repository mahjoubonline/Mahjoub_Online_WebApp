from flask import render_template
from flask_login import login_required, current_user
from . import admin_bp
# استيراد الموديلات من الحزمة المركزية لضمان عمل الربط مع قاعدة البيانات
from core.models import User, Supplier, Order 

@admin_bp.route('/dashboard')
@login_required  # حماية السيادة: الوصول للقائد فقط
def admin_dashboard():
    """
    لوحة التحكم المركزية (نظام الرقابة العليا) لمنصة محجوب أونلاين
    إدارة العمليات التجارية في الخوخة، عدن، المخا، وحيس
    """
    
    # تجهيز البيانات لتتوافق تماماً مع تصميم dashboard.html المهيب
    # تم تحديث القيم لتطابق المتغيرات التي صممتها في الواجهة
    context = {
        'orders_count': "1,250",       # إجمالي المبيعات (تظهر في بطاقة الصاروخ)
        's_count': "48",              # شركاء الترسانة - الموردين
        'total_balance': "15.5K",      # السيولة المركزية (بالدولار)
        'p_count': "12",               # طلبات قيد التدقيق (تظهر في بطاقة الميكروتشيب)
        'admin_name': current_user.username, # تحية القائد (علي محجوب)
        
        # بيانات سجل العمليات السيادية التي تملأ الجدول في أسفل الصفحة
        'transactions': [
            {
                'supplier_name': 'مورد عدن المركزي',
                'type': 'توريد بضائع',
                'amount': 2500,
                'date': '2026-05-02',
                'status': 'مكتمل'
            },
            {
                'supplier_name': 'شركة المخا للاستيراد',
                'type': 'سحب سيولة',
                'amount': -450,
                'date': '2026-05-01',
                'status': 'قيد التدقيق'
            },
            {
                'supplier_name': 'موزع الخوخة الرقمي',
                'type': 'تسوية عمولة',
                'amount': 120,
                'date': '2026-04-30',
                'status': 'مكتمل'
            }
        ]
    }
    
    # تمرير البيانات كمتغيرات مستقلة ليفهمها قالب Jinja2
    return render_template('dashboard.html', **context)
