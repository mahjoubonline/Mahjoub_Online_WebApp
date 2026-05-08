/**
 * Sovereign Engine v3.5 - محرك إدارة الموردين والموظفين
 * منصة محجوب أونلاين - سوقك الذكي
 */

// دالة الاستدعاء الرئيسي (Search Engine)
async function triggerSearch() {
    const query = document.getElementById('mainSearch').value;
    const province = document.getElementById('filterProvince').value;
    const district = document.getElementById('filterDistrict').value;
    const tier = document.getElementById('filterTier').value;
    const status = document.getElementById('filterStatus').value;

    const resultsArea = document.getElementById('resultsArea');
    const tableBody = document.getElementById('suppliersTableBody');
    const loader = document.getElementById('searchLoader');

    if (loader) loader.style.display = 'block';
    
    tableBody.innerHTML = '<tr><td colspan="7" class="py-4"><i class="fas fa-spinner fa-spin text-royal"></i> جاري استدعاء البيانات السيادية...</td></tr>';

    try {
        const params = new URLSearchParams({
            q: query,
            province: province,
            district: district,
            tier: tier,
            status: status
        });

        const response = await fetch(`/admin/api/suppliers/search?${params}`);
        const data = await response.json();

        tableBody.innerHTML = '';

        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7" class="py-4 text-muted">لا توجد نتائج مطابقة في سجلات الترسانة</td></tr>';
            return;
        }

        data.forEach(sup => {
            const row = `
                <tr id="row_${sup.id}" onclick="viewSupplier(${sup.id})" style="cursor:pointer;">
                    <td class="fw-bold text-royal">#${sup.sovereign_id || 'SUP_'+sup.id}</td>
                    <td>
                        <div class="fw-bold">${sup.trade_name}</div>
                        <small class="text-muted">${sup.owner_name}</small>
                    </td>
                    <td><small>${sup.province} - ${sup.district}</small></td>
                    <td><span class="badge bg-soft-royal text-royal border border-royal px-3">${sup.tier}</span></td>
                    <td>
                        <div class="small fw-bold text-success">${Number(sup.balance_yer).toLocaleString()} YER</div>
                        <div class="small text-primary">${Number(sup.balance_sar).toLocaleString()} SAR</div>
                        <div class="small text-warning">${Number(sup.balance_usd).toLocaleString()} USD</div>
                    </td>
                    <td>
                        <span class="badge rounded-pill px-3 ${getStatusClass(sup.status)}">
                            ${getStatusLabel(sup.status)}
                        </span>
                    </td>
                    <td>
                        <div class="btn-group" onclick="event.stopPropagation();">
                            <button class="btn btn-sm btn-outline-royal" onclick="viewSupplier(${sup.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="toggleStatus(${sup.id}, '${sup.status}')">
                                <i class="fas fa-power-off"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        });

    } catch (error) {
        console.error("Search Error:", error);
        tableBody.innerHTML = '<tr><td colspan="7" class="text-danger py-4">حدث خطأ في الاتصال بنواة النظام</td></tr>';
    } finally {
        if (loader) loader.style.display = 'none';
    }
}

// دالة جلب بيانات مورد محدد لفتح المودال
async function viewSupplier(supplierId) {
    const modalArea = document.getElementById('modalContentArea');
    const modalLoader = document.getElementById('modalLoader');
    
    if (modalLoader) modalLoader.style.display = 'block';
    if (modalArea) modalArea.style.opacity = '0.3';

    try {
        const response = await fetch(`/admin/api/supplier/${supplierId}`);
        const sup = await response.json();

        // تعبئة البيانات الأساسية
        document.getElementById('m_title').innerText = `🛡️ تعديل كيان: ${sup.trade_name}`;
        document.getElementById('m_owner_name').value = sup.owner_name;
        document.getElementById('m_trade_name').value = sup.trade_name;
        document.getElementById('m_province').value = sup.province;
        document.getElementById('m_district').value = sup.district;
        document.getElementById('m_bal_yer').value = sup.balance_yer;
        document.getElementById('m_bal_sar').value = sup.balance_sar;
        document.getElementById('m_bal_usd').value = sup.balance_usd;
        document.getElementById('m_tier').value = sup.tier;
        document.getElementById('m_status').value = sup.status;

        // تخزين المعرف الحالي
        document.getElementById('sovereignModal').setAttribute('data-current-id', supplierId);

        // جلب قائمة الموظفين (إذا تم تضمينهم في الـ JSON)
        loadStaffList(sup.staff || []);

        const modalElement = document.getElementById('sovereignModal');
        const myModal = bootstrap.Modal.getOrCreateInstance(modalElement);
        myModal.show();
    } catch (error) {
        alert("فشل في استدعاء بيانات الكيان من القاعدة");
    } finally {
        if (modalLoader) modalLoader.style.display = 'none';
        if (modalArea) modalArea.style.opacity = '1';
    }
}

// دالة حفظ التعديلات الشاملة (حفظ سيادي)
async function saveAllChanges() {
    const supId = document.getElementById('sovereignModal').getAttribute('data-current-id');
    const updateData = {
        owner_name: document.getElementById('m_owner_name').value,
        trade_name: document.getElementById('m_trade_name').value,
        province: document.getElementById('m_province').value,
        district: document.getElementById('m_district').value,
        balance_yer: document.getElementById('m_bal_yer').value,
        balance_sar: document.getElementById('m_bal_sar').value,
        balance_usd: document.getElementById('m_bal_usd').value,
        tier: document.getElementById('m_tier').value,
        status: document.getElementById('m_status').value,
        new_password: document.getElementById('m_new_pass') ? document.getElementById('m_new_pass').value : ''
    };

    try {
        const response = await fetch(`/admin/api/supplier/${supId}/update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        if (response.ok) {
            Swal.fire({ icon: 'success', title: 'تم التعميد', text: 'تم تحديث بيانات الكيان بنجاح', timer: 1500 });
            bootstrap.Modal.getInstance(document.getElementById('sovereignModal')).hide();
            triggerSearch(); // تحديث الجدول
        } else {
            throw new Error("Update Failed");
        }
    } catch (error) {
        Swal.fire({ icon: 'error', title: 'فشل التعميد', text: 'حدث خطأ أثناء حفظ البيانات' });
    }
}

// دالة تحميل قائمة الموظفين في المودال
function loadStaffList(staffArray) {
    const list = document.getElementById('staffList');
    list.innerHTML = '';
    if (!staffArray || staffArray.length === 0) {
        list.innerHTML = '<div class="text-center text-muted small py-4">لا يوجد موظفون مرتبطون حالياً</div>';
        return;
    }

    staffArray.forEach(s => {
        list.innerHTML += `
            <div class="d-flex justify-content-between align-items-center p-3 mb-2 bg-white rounded shadow-sm border-end border-royal border-3 animate__animated animate__fadeInRight">
                <div>
                    <div class="fw-bold small">${s.name}</div>
                    <span class="badge bg-light text-royal p-1" style="font-size: 10px;">${s.role}</span>
                </div>
                <div class="btn-group">
                    <button class="btn btn-sm text-primary" title="اتصال"><i class="fas fa-phone"></i></button>
                    <button class="btn btn-sm text-danger" onclick="removeStaff(${s.id})" title="فصل"><i class="fas fa-user-minus"></i></button>
                </div>
            </div>
        `;
    });
}

// وظائف مساعدة للتنسيق
function getStatusClass(status) {
    const map = { 'active': 'bg-success', 'suspended': 'bg-warning text-dark', 'audit': 'bg-info', 'banned': 'bg-danger' };
    return map[status] || 'bg-secondary';
}

function getStatusLabel(status) {
    const map = { 'active': 'نشط', 'suspended': 'موقف', 'audit': 'رقابة', 'banned': 'محظور' };
    return map[status] || 'غير محدد';
}

// تأخير البحث (Debounce) لتحسين الأداء
let debounceTimer;
function handleSearch(val) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        triggerSearch();
    }, 400);
}
