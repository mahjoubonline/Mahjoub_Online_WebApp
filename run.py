import os
import sys

# إجبار بايثون على إضافة المجلد الحالي للمسار
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

from core import create_app

app = create_app()

if __name__ == "__main__":
    # هذا السطر يضمن أن Railway سيجد البورت الصحيح
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
