from apps.models.admin_db import AdminUser # استيراد نموذج قاعدة البيانات

@auth_portal.route('/m7jb_sovereign_hq_v2_99x', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # المستخدم يدخل اسم المستخدم أو الهوية فقط
        username = request.form.get('username') 
        
        # 1. البحث عن المستخدم في قاعدة البيانات
        admin = AdminUser.query.filter_by(username=username).first()
        
        if not admin:
            flash("هوية غير معروفة في النظام السيادي.")
            return render_template('auth/login.html')
        
        # 2. جلب الهاتف المرتبط به تلقائياً
        phone = admin.phone_number
        
        # 3. توليد الرمز وإرساله كما في السابق
        otp_code = str(random.randint(100000, 999999))
        if AdminAuthService.initiate_login(phone, otp_code):
            session['otp_code'] = otp_code
            session['otp_phone'] = phone
            session['user_id'] = admin.id # حفظ الـ ID لإتمام الدخول لاحقاً
            return redirect(url_for('auth_portal.verify_otp_page'))
        else:
            flash("فشل التواصل مع بوابة الرسائل.")
            return render_template('auth/login.html')

    return render_template('auth/login.html')
