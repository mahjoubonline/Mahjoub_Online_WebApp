# coding: utf-8
# 📂 apps/data/financial_companies.py

"""
قائمة الشركات المالية وشركات الصرافة في اليمن
"""

FINANCIAL_COMPANIES = [
    # شركات الصرافة الكبرى
    {'id': 'haddad', 'name': 'أحمد الحداد وأخوانه للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'quteibi', 'name': 'شركة القطيبي للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'baseri', 'name': 'شركة البسيري للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_amri', 'name': 'شركة العمري للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_kharafi', 'name': 'شركة الخرافي للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_wahda', 'name': 'شركة الوحدة للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_aman', 'name': 'شركة الأمان للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_rayan', 'name': 'شركة الريان للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_saeed', 'name': 'شركة السعيد للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_madani', 'name': 'شركة المدني للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_hassan', 'name': 'شركة الحسن للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_hadi', 'name': 'شركة الهادي للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_buraq', 'name': 'شركة البراق للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_andalus', 'name': 'شركة الأندلس للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_mutawakkil', 'name': 'شركة المتوكل للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_sharafi', 'name': 'شركة الشرافي للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_ghurabi', 'name': 'شركة الغرابي للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    {'id': 'al_zubeiri', 'name': 'شركة الزبيري للصرافة', 'icon': 'fa-exchange-alt', 'type': 'صرافة'},
    
    # شركات التحويل المالي
    {'id': 'western_union', 'name': 'ويسترن يونيون (Western Union)', 'icon': 'fa-globe-americas', 'type': 'تحويل'},
    {'id': 'moneygram', 'name': 'ماني جرام (MoneyGram)', 'icon': 'fa-globe-americas', 'type': 'تحويل'},
    {'id': 'riyal', 'name': 'شركة ريال للتحويل المالي', 'icon': 'fa-money-bill-wave', 'type': 'تحويل'},
    {'id': 'al_amal', 'name': 'شركة الأمل للتحويل المالي', 'icon': 'fa-money-bill-wave', 'type': 'تحويل'},
    {'id': 'al_najah', 'name': 'شركة النجاح للتحويل المالي', 'icon': 'fa-money-bill-wave', 'type': 'تحويل'},
    {'id': 'al_salam', 'name': 'شركة السلام للتحويل المالي', 'icon': 'fa-money-bill-wave', 'type': 'تحويل'},
    
    # شركات التمويل
    {'id': 'al_kuraimi', 'name': 'شركة الكريمي للتمويل', 'icon': 'fa-hand-holding-usd', 'type': 'تمويل'},
    {'id': 'al_tadhamon', 'name': 'شركة تضامن للتمويل', 'icon': 'fa-hand-holding-usd', 'type': 'تمويل'},
    {'id': 'al_aman_trust', 'name': 'شركة الأمانة للتمويل', 'icon': 'fa-hand-holding-usd', 'type': 'تمويل'},
    {'id': 'al_basheer', 'name': 'شركة البشير للتمويل', 'icon': 'fa-hand-holding-usd', 'type': 'تمويل'},
    
    # شركات الاستثمار
    {'id': 'al_istithmar', 'name': 'شركة الاستثمار اليمنية', 'icon': 'fa-chart-line', 'type': 'استثمار'},
    {'id': 'al_ahli', 'name': 'شركة الأهلي للاستثمار', 'icon': 'fa-chart-line', 'type': 'استثمار'},
    {'id': 'al_razi', 'name': 'شركة الرازي للاستثمار', 'icon': 'fa-chart-line', 'type': 'استثمار'},
    
    # أخرى
    {'id': 'other', 'name': 'شركة أخرى', 'icon': 'fa-building', 'type': 'أخرى'}
]

# ✅ قائمة بأسماء الشركات فقط (للقوائم المنسدلة)
FINANCIAL_COMPANIES_LIST = [comp['name'] for comp in FINANCIAL_COMPANIES]

# ✅ قائمة بالشركات حسب النوع
def get_companies_by_type(comp_type):
    return [comp for comp in FINANCIAL_COMPANIES if comp['type'] == comp_type]

# ✅ دالة للحصول على أيقونة الشركة
def get_company_icon(company_name):
    for comp in FINANCIAL_COMPANIES:
        if comp['name'] == company_name:
            return comp['icon']
    return 'fa-building'

# ✅ دالة للحصول على معرف الشركة
def get_company_id(company_name):
    for comp in FINANCIAL_COMPANIES:
        if comp['name'] == company_name:
            return comp['id']
    return None

# ✅ دالة للبحث عن شركة
def search_company(query):
    query = query.lower()
    return [comp for comp in FINANCIAL_COMPANIES if query in comp['name'].lower()]

# ✅ دالة للحصول على نوع الشركة
def get_company_type(company_name):
    for comp in FINANCIAL_COMPANIES:
        if comp['name'] == company_name:
            return comp['type']
    return 'أخرى'
