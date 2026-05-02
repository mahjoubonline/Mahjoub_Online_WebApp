from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_bp
from core.models import User, Supplier, Order  # استيراد الموديلات من الحزمة المركزية

@admin_bp.route('/dashboard')
@login_required  # حماية السيادة: الوصول للقائد فقط
def admin_dashboard():
    """
    لوحة التحكم المركزية (نظام الرقابة العليا) لمنصة محجوب أونلاين
    """
    
    # تجهيز البيانات لتتوافق تماماً مع متغيرات ملف dashboard.html الخاص بك
    # ملاحظة: القيم هنا ثابتة حالياً، ويمكنك لاحقاً ربطها بـ Query من قاعدة البيانات
    context = {
        'orders_count': "1,250",       # إجمالي المبيعات (تظهر في البطاقة الأولى)
        's_count': "48",              # شركاء الترسانة - الموردين
        'total_balance': "15.5K",      # السيولة المركزية (بالدولار)
        'p_count': "12",               # طلبات قيد التدقيق
        'admin_name': current_user.username, # تحية القائد (علي محجوب)
        
        # بيانات سجل العمليات السيادية للجدول (Transactions)
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
    
    # تمرير القاموس بالكامل إلى القالب ليفككه Jinja2 تلقائياً
    return render_template('dashboard.html', **context)

@admin_bp.route('/logout')
@login_required
def logout():
    """
    الخروج الآمن من نظام الرقابة
    """
    logout_user()
    flash('تم تسجيل الخروج من الترسانة بنجاح.', 'info')
    return redirect(url_for('admin.admin_login'))
