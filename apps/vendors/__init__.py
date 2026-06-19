from flask import Flask

def create_app():
    app = Flask(__name__)

    # المبدأ: لا نكتب أكواد، فقط نستدعي "المدراء"
    from apps.admin_dashboard import admin_manager
    from apps.vendors import vendors_manager
    from apps.orders import orders_manager
    # يمكنك إضافة أي عدد من المصانع هنا لاحقاً دون أي ضغط
    
    # التسجيل:
    app.register_blueprint(admin_manager)
    app.register_blueprint(vendors_manager)
    app.register_blueprint(orders_manager)

    return app
