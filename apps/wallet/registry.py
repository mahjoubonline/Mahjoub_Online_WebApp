# 📂 apps/wallet/registry.py

# قم بتغيير اسم الدالة هنا لتطابق ما يبحث عنه الـ Auto-Discovery
def register_module(app): 
    # تسجيل البلوبرينت
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح.")
