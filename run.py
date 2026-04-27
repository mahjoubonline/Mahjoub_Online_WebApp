from core import app

if __name__ == '__main__':
    # Railway يحدد المنفذ تلقائياً، ولكن 5000 ممتاز للتطوير
    app.run(host='0.0.0.0', port=5000)
