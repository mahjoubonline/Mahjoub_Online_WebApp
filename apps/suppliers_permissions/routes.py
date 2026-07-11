{% extends 'suppliers/base.html' %}

{% block content %}
<div class="container-fluid py-4" style="direction: rtl; text-align: right; font-family: sans-serif;">

    <div class="d-flex align-items-center mb-4">
        <button onclick="window.history.back()" class="btn btn-sm btn-outline-secondary me-3">
            <i class="fa fa-arrow-right"></i> رجوع
        </button>
        <h3 class="fw-bold m-0" style="color: #333;">إدارة صلاحيات الموظفين</h3>
    </div>

    <button class="btn btn-primary mb-4" data-bs-toggle="modal" data-bs-target="#addStaffModal" style="background-color: #5b4cd1; border: none;">
        <i class="fa fa-plus-circle me-2"></i> إضافة موظف جديد
    </button>

    <div class="table-responsive bg-white p-3 shadow-sm rounded">
        <table class="table table-hover align-middle">
            <thead class="table-light">
                <tr>
                    <th>#</th>
                    <th>اسم المستخدم</th>
                    <th>رقم الهاتف</th>
                    <th>تاريخ الإنشاء</th>
                    <th>الحالة</th>
                    <th>الإجراءات</th>
                </tr>
            </thead>
            <tbody>
                {% for staff in staff_list %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td class="fw-bold" style="color: #6c5ce7;">{{ staff.username }}</td>
                    <td>{{ staff.search_phone }}</td>
                    <td>{{ staff.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                    <td><span class="badge bg-success">نشط</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary"><i class="fa fa-edit"></i></button>
                        <button class="btn btn-sm btn-outline-danger"><i class="fa fa-trash"></i></button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<div class="modal fade" id="addStaffModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5>إضافة موظف</h5></div>
            <form method="POST">
                <div class="modal-body">
                    <input type="text" name="username" class="form-control mb-2" placeholder="اسم المستخدم" required>
                    <input type="text" name="phone" class="form-control mb-2" placeholder="رقم الهاتف" required>
                    <input type="password" name="password" class="form-control" placeholder="كلمة المرور" required>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">حفظ</button>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
    .badge { padding: 0.5em 1em; }
    .table-hover tbody tr:hover { background-color: #f8f9fa; }
</style>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
{% endblock %}
