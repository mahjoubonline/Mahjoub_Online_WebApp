# coding: utf-8
from flask import Blueprint

# تأسيس المخطط المالي السيادي للمحافظ والتسويات
wallet_blueprint = Blueprint(
    'wallet',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from apps.wallet import routes
