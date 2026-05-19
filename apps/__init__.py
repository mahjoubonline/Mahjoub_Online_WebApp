<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}القيادة المركزية | محجوب أونلاين{% endblock %}</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    
    <style>
        :root { --royal-purple: #632C8F; --deep-black: #08020d; --mahjoub-gold: #D4AF37; }
        body { font-family: 'Cairo', sans-serif; background: #f0f2f5; margin: 0; display: flex; direction: rtl; }
        /* باقي الستايل كما هو في كودك الأصلي */
    </style>
</head>
<body>

    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <img src="https://cdn.qumra.cloud/media/67f7f6d5f0b82f44a47bf845/1770229315912-117966978.webp" class="logo-img" alt="Logo">
            <h2 class="text-white h5 fw-bold mb-1">محجوب أونلاين</h2>
        </div>

        <nav class="nav-menu">
            <a href="{{ url_for('admin_dashboard.dashboard_home') }}" class="nav-link">
                <i class="fas fa-chart-line ms-3"></i> <span>مركز القيادة</span>
            </a>

            <div class="dropdown-section">
                <button class="dropdown-btn" onclick="toggleDropdown('supplierDropdown', 'supplierArrow')">
                    <i class="fas fa-handshake ms-3"></i> <span>شركاء النجاح</span>
                    <i class="fas fa-chevron-left" id="supplierArrow"></i>
                </button>
                <div class="dropdown-container" id="supplierDropdown">
                    <a href="{{ url_for('add_supplier.add_supplier_submit') }}">
                        <i class="fas fa-user-plus ms-2"></i> تعميد مورد جديد
                    </a>
                    <a href="{{ url_for('add_supplier.admin_suppliers_list') }}">
                        <i class="fas fa-database ms-2"></i> سجل الموردين
                    </a>
                </div>
            </div>

            <div class="dropdown-section">
                <button class="dropdown-btn" onclick="toggleDropdown('walletDropdown', 'walletArrow')">
                    <i class="fas fa-wallet ms-3"></i> <span>الفضاء المالي</span>
                    <i class="fas fa-chevron-left" id="walletArrow"></i>
                </button>
                <div class="dropdown-container" id="walletDropdown">
                    <a href="{{ url_for('admin_wallet.wallet_overview') }}">
                        <i class="fas fa-vault ms-2"></i> حوكمة وفحص المحافظ
                    </a>
                </div>
            </div>

            <a href="{{ url_for('admin_dashboard.system_settings') }}" class="nav-link">
                <i class="fas fa-shield-halved ms-3"></i> <span>إعدادات السيادة</span>
            </a>

            <a href="{{ url_for('auth_portal.logout') }}" class="nav-link text-danger mt-auto">
                <i class="fas fa-power-off ms-3"></i> <span>تسجيل خروج آمن</span>
            </a>
        </nav>
    </aside>

    <main class="main-wrapper">
        <header class="top-bar">
            <h4 class="mb-0 fw-bold text-dark">{% block header_title %}مركز المراقبة{% endblock %}</h4>
            <div class="user-badge">{{ current_user.username if current_user else 'المؤسس' }}</div>
        </header>
        <div class="p-4 content-area">{% block content %}{% endblock %}</div>
    </main>
</body>
</html>
