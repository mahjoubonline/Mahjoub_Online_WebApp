from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return """
    <div style="text-align:center; margin-top:100px; font-family:Arial;">
        <h1 style="color:#D4AF37;">Mahjoub Online - محجوب أونلاين</h1>
        <p style="color:#555;">النظام يعمل بنجاح على Railway!</p>
        <div style="color:gold; font-size:50px;">★</div>
    </div>
    """

if __name__ == "__main__":
    # Railway يطلب تشغيل التطبيق على البورت 8080 غالباً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
