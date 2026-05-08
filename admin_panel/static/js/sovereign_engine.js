// دالة الاستدعاء الرئيسي (Search Engine)
async function triggerSearch() {
    const query = document.getElementById('mainSearch').value;
    const province = document.getElementById('filterProvince').value;
    const district = document.getElementById('filterDistrict').value;
    const tier = document.getElementById('filterTier').value;
    const status = document.getElementById('filterStatus').value;

    // إظهار منطقة النتائج وإخفاء حالة الفراغ
    const resultsArea = document.getElementById('resultsArea');
    const emptyState = document.getElementById('emptyState');
    const tableBody = document.getElementById('suppliersTableBody');

    if (!query && !province && !district && !tier && !status) {
        resultsArea.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    tableBody.innerHTML = '<tr><td colspan="7"><i class="fas fa-spinner fa-spin"></i> جاري استدعاء البيانات من القاعدة...</td></tr>';
    resultsArea.style.display = 'block';
    emptyState.style.display = 'none';

    try {
        // إرسال الطلب إلى السيرفر (يجب أن يكون لديك Route في Flask بهذا الاسم)
        const response = await fetch(`/admin/api/suppliers/search?q=${query}&province=${province}&district=${district}&tier=${tier}&status=${status}`);
        const data = await response.json();

        tableBody.innerHTML = '';

        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7" class="py-4 text-muted">لا توجد نتائج مطابقة في سجلات الترسانة</td></tr>';
            return;
        }

        data.forEach(sup => {
            const row = `
                <tr id="row_${sup.id}">
                    <td class="fw-bold text-royal">#SUP_${sup.id}</td>
                    <td>
                        <div class="fw-bold">${sup.trade_name}</div>
                        <small class="text-muted">${sup.owner_name}</small>
                    </td>
                    <td><small>${sup.province} - ${sup.district}</small></td>
                    <td><span class="badge bg-soft-royal text-royal border border-royal">${sup.tier}</span></td>
                    <td>
                        <div class="small fw-bold text-success">${sup.balance_yer} YER</div>
                        <div class="small text-primary">${sup.balance_sar} SAR</div>
                        <div class="small text-warning">${sup.balance_usd} USD</div>
                    </td>
                    <td>
                        <span class="badge ${sup.status === 'active' ? 'bg-success' : 'bg-danger'}">
                            ${sup.status === 'active' ? 'نشط' : 'موقف'}
                        </span>
                    </td>
                    <td>
                        <div class="btn-group">
                            <button class="btn btn-sm btn-outline-royal" onclick="viewSupplier(${sup.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="toggleStatus(${sup.id})">
                                <i class="fas fa-power-off"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        });

    } catch (error) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-danger">حدث خطأ في الاتصال بالخادم</td></tr>';
    }
}

// دالة جلب بيانات مورد محدد لفتح المودال
async function viewSupplier(supplierId) {
    try {
        const response = await fetch(`/admin/api/suppliers/${supplierId}`);
        const sup = await response.json();

        // تعبئة بيانات المودال
        document.getElementById('m_title').innerText = `🛡️ تعديل كيان: ${sup.trade_name}`;
        document.getElementById('m_owner_name').value = sup.owner_name;
        document.getElementById('m_username').value = sup.username;
        document.getElementById('m_province').value = sup.province;
        document.getElementById('m_district').value = sup.district;
        document.getElementById('m_bal_yer').value = sup.balance_yer;
        document.getElementById('m_bal_sar').value = sup.balance_sar;
        document.getElementById('m_bal_usd').value = sup.balance_usd;
        document.getElementById('m_tier').value = sup.tier;

        // تخزين معرف المورد في المودال لاستخدامه عند الحفظ
        document.getElementById('sovereignModal').setAttribute('data-current-id', supplierId);

        // جلب قائمة الموظفين التابعين له
        loadStaffList(sup.staff);

        var myModal = new bootstrap.Modal(document.getElementById('sovereignModal'));
        myModal.show();
    } catch (error) {
        alert("فشل في جلب بيانات المورد");
    }
}

function loadStaffList(staffArray) {
    const list = document.getElementById('staffList');
    list.innerHTML = '';
    if (!staffArray || staffArray.length === 0) {
        list.innerHTML = '<p class="text-center text-muted small py-3">لا يوجد موظفون مرتبطون حالياً</p>';
        return;
    }

    staffArray.forEach(s => {
        list.innerHTML += `
            <div class="d-flex justify-content-between align-items-center p-2 mb-2 bg-light rounded border-end border-royal border-3">
                <div>
                    <div class="small fw-bold">${s.name}</div>
                    <small class="text-muted">${s.role}</small>
                </div>
                <button class="btn btn-sm text-danger" onclick="removeStaff(${s.id})"><i class="fas fa-trash"></i></button>
            </div>
        `;
    });
}
