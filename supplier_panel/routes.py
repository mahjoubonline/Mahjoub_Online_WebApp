# صفحة دخول المورد
@supplier_bp.route('/login')
def login():
    return render_template('supplier_panel/supplier_login.html')

# صفحة انتظار التعميد (Waiting Approval)
@supplier_bp.route('/pending')
def pending():
    return render_template('supplier_panel/waiting_approval.html')

# صفحة إضافة منتج جديد
@supplier_bp.route('/add-product')
@login_required
def add_product():
    return render_template('supplier_panel/add_product.html')
