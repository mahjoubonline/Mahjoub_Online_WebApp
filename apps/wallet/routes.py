from flask import Blueprint, render_template, request
from apps.models.wallet import Wallet  # تأكد من استيراد الموديل الصحيح
from apps import db

wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

@wallet_app.route('/wallet', methods=['GET'])
def dashboard():
    search = request.args.get('search', '')
    
    # استعلام لجلب المحافظ مع بيانات المورد المرتبطة بها
    query = Wallet.query
    
    if search:
        # البحث في اسم المورد (بافتراض وجود علاقة wallet.supplier)
        query = query.join(Wallet.supplier).filter(
            Supplier.trade_name.contains(search) | 
            Supplier.id.contains(search)
        )
        
    wallets = query.all()
    
    return render_template('admin/wallet_app.html', wallets=wallets)

@wallet_app.route('/wallet/view/<int:supplier_id>')
def view_wallet(supplier_id):
    # كود لجلب تفاصيل محفظة مورد معين
    wallet = Wallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    return render_template('admin/view_wallet.html', wallet=wallet)
