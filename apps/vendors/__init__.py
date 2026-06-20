from apps.vendors.routes import vendors_bp
app.register_blueprint(vendors_bp, url_prefix='/vendors')
