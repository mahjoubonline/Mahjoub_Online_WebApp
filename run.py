import os
from core import create_app

app = create_app()

if __name__ == '__main__':
    # Railway يمرر المنفذ عبر متغير PORT، وإذا لم يجده سيستخدم 8080 كما حددت أنت
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
