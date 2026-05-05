# core/extensions.py
from flask_sqlalchemy import SQLAlchemy

# نحن هنا نجهز كائن قاعدة البيانات ليكون متاحاً لكل النظام
db = SQLAlchemy()
