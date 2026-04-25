from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required 

# --- 1. مسار تسجيل الدخول اللامركزي ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    # منع التداخل: إذا كان المستخدم مسجل دخوله بالفعل
    if current_user.is_authenticated:
        # إذا كان يمتلك صفات المورد (محفظة)، نرسله للداشبورد مباشرة
        if hasattr(current_user, 'wallet_balance'):
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            # إذا كان أدمن يحاول الدخول لبوابة المورد، ننهي جلسته لفتح المجال للهوية الجديدة
            logout_user() 

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى ملء كافة الحقول السيادية للدخول.', 'warning')
            return render_template('supplier_login.html')

        # التحقق من الهوية عبر المحقق الخارجي (auth_logic)
        message, category, supplier = verify_supplier_credentials(username, password)
        
        if supplier: 
            # 🛡️ الربط السيادي: نخبر النظام أن صاحب هذه الجلسة هو "مورد"
            # هذا السطر هو مفتاح الحل لمنع التداخل مع لوحة الإدارة
            session['user_type'] = 'supplier'
            
            login_user(supplier)
            flash(f'تم الولوج بنجاح.. أهلاً بك يا {supplier.name}', 'success')
            
            # التوجه للداشبورد (سيتكفل الحارس @sovereign_approval_required بفحصه هناك)
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message, category)
            
    return render_template('supplier_login.html')

# --- 2. لوحة التحكم (الترسانة الرقمية) ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required # 🛡️ هذا الحارس سيقوم بتحويله لـ /waiting-room إذا لم يُعمد
def dashboard():
    from core.models.product import Product
    
    try:
        # فحص الرتبة: للتأكد أن المستخدم ليس أدمن تسلل لهذا المسار
        if not hasattr(current_user, 'wallet_balance'):
            session.pop('user_type', None)
            logout_user()
            flash('عذراً، هذه المنطقة مخصصة لشركاء النجاح فقط.', 'danger')
            return redirect(url_for('supplier_panel.login'))
            
        # جلب المنتجات المرتبطة بهذا المورد فقط
        try:
            # تأكد أن الموديل Product يحتوي على حقل supplier_id
            my_products = Product.query.filter_by(supplier_id=current_user.id).all()
        except Exception as db_error:
            print(f"⚠️ تنبيه في قاعدة البيانات: {db_error}")
            my_products = []
            
        # استدعاء القالب (dashboard.html) الموجود في مجلد templates الخاص بالمورد
        return render_template('dashboard.html', products=my_products)
        
    except Exception as e:
        print(f"❌ خطأ داخلي في لوحة المورد: {e}")
        # إظهار رسالة خطأ واضحة في حال الانهيار (500)
        return f"خطأ في النظام (500): {str(e)}", 500

# --- 3. صفحة الانتظار (البرزخ الرقمي) ---
@supplier_bp.route('/waiting-room')
@login_required
def waiting_room():
    """
    هذا المسار يستقر فيه المورد حتى يتم اعتماده سيادياً من قبل الإدارة
    """
    # إذا تم اعتماده وهو هنا، ارسله للداشبورد فوراً
    if hasattr(current_user, 'is_approved') and current_user.is_approved:
        return redirect(url_for('supplier_panel.dashboard'))
    
    # استدعاء قالب صفحة الانتظار
    return render_template('waiting_approval.html')

# --- 4. خروج المورد وتأمين الترسانة ---
@supplier_bp.route('/logout')
@login_required
def logout():
    # تنظيف الجلسة السيادية عند الخروج
    session.pop('user_type', None)
    logout_user()
    flash('تم تأمين الجلسة وتشفير الخروج بنجاح.', 'info')
    return redirect(url_for('supplier_panel.login'))
