# apps/__init__.py

def create_app():
    app = Flask(__name__)
    
    # تسجيل الـ Blueprint الخاص بالتقارير
    from apps.statement import statement_blueprint
    app.register_blueprint(statement_blueprint, url_prefix='/statement')
    
    # ... بقية التسجيلات ...
    return app
