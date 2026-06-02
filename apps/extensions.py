# coding: utf-8
# 🛡️ كبسولة الملحقات السيادية - منصة محجوب أونلاين 2026
# هذا الملف يعزل كائنات النظام الأساسية لضمان حوكمة البيانات ومنع التداخل الدائري (Circular Imports)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 1️⃣ إدارة وحوكمة قاعدة البيانات اللامركزية للمنصة
db = SQLAlchemy()

# 2️⃣ إدارة الجلسات الرقمية والتحقق من الهوية السيادية
login_manager = LoginManager()

# ⚙️ التكوين الأمني الافتراضي لإدارة الهوية
# تخصيص تنبيه الحماية الجداري عند محاولة الوصول لصفحة مقيدة دون نفاذ رقمي مسبق
login_manager.login_message = "تنبيه أمني: يرجى توثيق هويتك الرقمية أولاً للولوج إلى هذه المنطقة السيادية."
login_manager.login_message_category = "warning"
