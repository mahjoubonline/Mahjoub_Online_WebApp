def format_price(amount, currency='YER'):
    """
    تنسيق السعر ليظهر بشكل احترافي مع رمز العملة.
    """
    if amount is None:
        return "0.00"
    return f"{amount:,.2f} {currency}"

def convert_currency(amount, rate):
    """
    تحويل المبلغ بناءً على سعر الصرف المعطى.
    مفيد عند استيراد منتجات بأسعار مختلفة (سعودي/دولار).
    """
    if not amount or not rate:
        return amount
    return amount * rate

def calculate_commission(price, commission_rate=0.05):
    """
    حساب عمولة المنصة (الافتراضي 5%).
    تغيير النسبة هنا سيغيرها في كامل المنصة فوراً.
    """
    return price * commission_rate
