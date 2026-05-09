import os
import base64
import json
from datetime import datetime, date
from decimal import Decimal
from github import Github, GithubException

class ArchiveManager:
    """
    مدير الأرشفة السيادية المطور v4.0 - منصة محجوب أونلاين
    المحرك الآن يستخدم PyGithub لضمان الاستقرار مع المستودعات الخاصة
    """

    def __init__(self):
        # جلب التوكن من بيئة Railway
        self.token = os.getenv('SOVEREIGN_ASSETS_TOKEN')
        self.repo_name = "alimohm/Mahjoub-Sovereign-Assets"
        
        # تهيئة الاتصال بمكتبة PyGithub
        if self.token:
            self.gh = Github(self.token)
        else:
            self.gh = None
            print("⚠️ تنبيه سيادي: SOVEREIGN_ASSETS_TOKEN غير معرف!")

    def _serialize_data(self, obj):
        """
        معالج التناسق: تحويل أنواع البيانات المعقدة (Decimal, DateTime) إلى نصوص
        لحل مشكلة فشل تحويل بيانات الموردين إلى JSON.
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    def generate_path(self, entity_id, folder_name="Registry"):
        """ توليد مسار لاتيني متوافق مع معايير الـ API الدولية """
        now = datetime.now()
        return f"{entity_id}/{now.year}/{now.month:02d}/{now.day:02d}/{folder_name}"

    def archive_data_as_json(self, data_dict, filename, entity_id, folder_name="Daily_Logs"):
        """
        الأرشفة الاحترافية للبيانات والسجلات
        """
        if not self.gh:
            return False

        try:
            repo = self.gh.get_repo(self.repo_name)
            target_path = f"{self.generate_path(entity_id, folder_name)}/{filename}.json"
            
            # تحويل القاموس إلى JSON مع معالجة الحقول المالية والتواريخ
            json_content = json.dumps(
                data_dict, 
                indent=4, 
                ensure_ascii=False, 
                default=self._serialize_data
            )

            commit_message = f"Sovereign Record - ID: {entity_id} - {datetime.now().strftime('%Y-%m-%d')}"

            # الرفع الذكي: إنشاء الملف أو تحديثه إذا كان موجوداً (يتعامل مع المجلدات المحذوفة تلقائياً)
            try:
                # محاولة جلب الملف إذا كان موجوداً للحصول على الـ SHA
                contents = repo.get_contents(target_path)
                repo.update_file(contents.path, commit_message, json_content, contents.sha)
                print(f"✅ تم تحديث السجل السيادي: {target_path}")
            except:
                # إذا لم يكن موجوداً، يتم إنشاؤه لأول مرة
                repo.create_file(target_path, commit_message, json_content)
                print(f"✅ تم إنشاء سجل سيادي جديد: {target_path}")
            
            return True

        except GithubException as ge:
            print(f"❌ فشل بروتوكول GitHub: {ge.data.get('message')}")
            return False
        except Exception as e:
            print(f"❌ خطأ غير متوقع في محرك الأرشفة: {str(e)}")
            return False

# تصدير النسخة المفردة للعمل في كافة أنحاء الترسانة
archive_sys = ArchiveManager()
