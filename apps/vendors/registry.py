import importlib
import os

def create_app():
    app = Flask(__name__)
    
    # محرك البحث الديناميكي عن الوحدات
    apps_dir = os.path.join(app.root_path, 'apps')
    for folder in os.listdir(apps_dir):
        registry_path = f"apps.{folder}.registry"
        try:
            # محاولة استيراد ملف registry.py من كل مجلد تلقائياً
            module = importlib.import_module(registry_path)
            if hasattr(module, 'register_vendors_module'):
                module.register_vendors_module(app)
        except ImportError:
            continue # تخطي المجلدات التي لا تحتوي على registry.py
            
    return app
