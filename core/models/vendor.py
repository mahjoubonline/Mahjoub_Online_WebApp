from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Vendor(models.Model):
    # --- الربط الأساسي مع المستخدم ---
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='vendor_profile',
        verbose_name="حساب المستخدم"
    )

    # --- بيانات الهوية والملك ---
    owner_name = models.CharField(max_length=255, verbose_name="اسم المالك الكامل")
    id_type = models.CharField(max_length=100, verbose_name="نوع الهوية")
    id_card_number = models.CharField(max_length=50, verbose_name="رقم الهوية / السجل التجاري")
    
    # --- بيانات المنشأة والنشاط ---
    trade_name = models.CharField(max_length=255, verbose_name="الاسم التجاري للمنشأة")
    activity_type = models.CharField(max_length=100, verbose_name="نوع النشاط التجاري")
    
    # --- البيانات الجغرافية والاتصال ---
    # ملاحظة: تعكس هذه الحقول نطاق عملياتك في اليمن (الخوخة، عدن، المخا، إلخ)
    province = models.CharField(max_length=100, verbose_name="المحافظة")
    district = models.CharField(max_length=100, verbose_name="المديرية")
    address_detail = models.CharField(max_length=500, verbose_name="العنوان بالتفصيل")
    
    phone_regex = RegexValidator(regex=r'^7\d{8}$', message="يجب إدخال رقم هاتف يمني صحيح يبدأ بـ 7")
    phone = models.CharField(validators=[phone_regex], max_length=9, verbose_name="رقم الهاتف")

    # --- الربط المالي والسيادي ---
    # الرقم السيادي يتم توليده برمجياً أو عبر الـ ID التلقائي
    e_wallet = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        verbose_name="رقم المحفظة السيادي"
    )
    
    FINANCE_CHOICES = [
        ('banks', 'بنوك إسلامية'),
        ('exchange', 'شركات صرافة'),
    ]
    fin_type = models.CharField(max_length=20, choices=FINANCE_CHOICES, default='banks', verbose_name="تصنيف الجهة المالية")
    bank_name = models.CharField(max_length=150, verbose_name="اسم البنك / شركة الصرافة")
    bank_acc = models.CharField(max_length=100, verbose_name="رقم الحساب البنكي")

    # --- بيانات النظام ---
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التعميد")
    is_verified = models.BooleanField(default=True, verbose_name="حالة التعميد السيادي")

    class Meta:
        verbose_name = "مورد سيادي"
        verbose_name_plural = "الموردون السياديون"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trade_name} - {self.e_wallet}"

    def save(self, *args, **kwargs):
        """
        منطق الربط التلقائي:
        يتم جعل رقم المحفظة مطابقاً للرقم التعريفي (Primary Key) لضمان الربط السيادي.
        """
        super().save(*args, **kwargs)
        if not self.e_wallet:
            # استخدام الرقم التعريفي كقيمة للمحفظة السيادية بعد الحفظ الأول
            self.e_wallet = str(self.id).zfill(6) # مثال: 000001
            # تحديث الحقل فقط لتجنب التكرار اللانهائي (Recursion)
            Vendor.objects.filter(pk=self.pk).update(e_wallet=self.e_wallet)
