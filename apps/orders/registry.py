{% extends "admin/base.html" %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>إضافة منتج جديد</h3>
        <a href="{{ url_for('admin_product.manage_products') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-right"></i> إلغاء
        </a>
    </div>

    <div class="card shadow-sm border-0" style="border-top: 4px solid var(--mahjoub-gold);">
        <div class="card-body">
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">اسم المنتج</label>
                    <input type="text" class="form-control" name="title" required>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">السعر</label>
                        <input type="number" class="form-control" name="price" step="0.01" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">الكمية</label>
                        <input type="number" class="form-control" name="quantity" required>
                    </div>
                </div>
                <button type="submit" class="btn btn-mahjoub-gold w-100">حفظ المنتج</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
