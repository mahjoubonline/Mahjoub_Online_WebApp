# مثال لصفحة الدخول
@admin_bp.route('/login')
def login():
    return render_template('admin_panel/login.html')

# مثال لإدارة الموردين (الصفحة الجديدة التي أضفتها)
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    return render_template('admin_panel/admin_suppliers_management.html')

# مثال لمحفظة الأموال
@admin_bp.route('/wallets')
@login_required
def wallets():
    return render_template('admin_panel/wallets.html')
