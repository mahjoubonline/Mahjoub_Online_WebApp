import requests, base64, os

from urllib.parse import quote

from datetime import datetime

from config import Config



class ArchiveManager:

    def __init__(self):

        self.token = Config.GITHUB_TOKEN.strip()

        self.repo = Config.GITHUB_REPO

        self.base_url = f"https://api.github.com/repos/{self.repo}/contents/Main_Archive"

        self.headers = {

            "Authorization": f"token {self.token}",

            "Accept": "application/vnd.github.v3+json"

        }



    def upload_document(self, s_id, u_id, doc_t, file_d, ext=".jpg", is_txt=False):

        """

        رفع الوثيقة إلى GitHub وإرجاع المسار (Path) لاستخدامه في العرض أو الحذف.

        """

        try:

            now = datetime.now()

            year, month, day = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")

            time_now = now.strftime("%H-%M-%S-%f") 

            

            # بناء المسار الهرمي السيادي

            path = f"{s_id}/{year}/{month}/{day}/{u_id}_{doc_t}_{time_now}{ext}"

            url = f"{self.base_url}/{quote(path)}"

            

            if is_txt:

                content_bytes = str(file_d).encode('utf-8')

            else:

                content_bytes = file_d



            content_base64 = base64.b64encode(content_bytes).decode('utf-8')

            

            payload = {

                "message": f"🛡️ Archiving System - ID: {s_id} - {u_id}",

                "content": content_base64,

                "branch": "main"

            }

            

            response = requests.put(url, json=payload, headers=self.headers)

            

            if response.status_code in [200, 201]:

                print(f"✅ تم الرفع بنجاح: {path}")

                return path  # نرجع المسار لنتمكن من حذفه لاحقاً

            else:

                print(f"⚠️ فشل الرفع لـ GitHub: {response.status_code}")

                return None

                

        except Exception as e: 

            print(f"❌ خطأ فني في الأرشفة: {e}")

            return None



    def delete_temporary_file(self, github_path):

        """

        🚀 المشرط الجراحي: حذف صور المنتجات بعد النشر النهائي في المتجر.

        """

        try:

            # 1. جلب بيانات الملف للحصول على بصمة الـ SHA (مطلوبة للحذف)

            url = f"{self.base_url}/{quote(github_path)}"

            get_res = requests.get(url, headers=self.headers)

            

            if get_res.status_code == 200:

                file_sha = get_res.json().get('sha')

                

                # 2. تنفيذ طلب الحذف الفعلي

                payload = {

                    "message": f"♻️ Auto-Cleanup: Deleting temporary product image {github_path}",

                    "sha": file_sha,

                    "branch": "main"

                }

                del_res = requests.delete(url, json=payload, headers=self.headers)

                

                if del_res.status_code == 200:

                    print(f"✅ تم تنظيف الأرشيف وحذف الملف المؤقت بنجاح.")

                    return True

            return False

        except Exception as e:

            print(f"❌ خطأ أثناء عملية التنظيف: {e}")

            return False



    def upload_full_package(self, data, files):

        """أرشفة بيانات المورد (دائمة)"""

        s_id = data.get('supplier_id') or data.get('vendor_uid') or "Unknown_ID"

        profile = self._generate_text_log(data)

        # الملف النصي (دائم)

        self.upload_document(s_id, "PROFILE", "Details", profile, ".txt", True)

        

        for i, file in enumerate(files, start=1):

            if file and file.filename:

                ext = os.path.splitext(file.filename)[1]

                data_bytes = file.read()

                if data_bytes:

                    # المرفقات (دائمة)

                    self.upload_document(s_id, f"DOC_{i}", "Identity", data_bytes, ext)

                file.seek(0)



    def _generate_text_log(self, d):

        return f"""

        ========================================

        🛡️ السجل السيادي للمورد: {d.get('supplier_id', 'N/A')}

        ========================================

        التوقيت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        الحساب: {d.get('username', 'غير محدد')} 

        المالك: {d.get('full_name', 'غير محدد')}

        الموقع: {d.get('province', 'غير محدد')} - {d.get('district', 'غير محدد')}

        البنك: {d.get('bank_name', 'غير محدد')} - {d.get('bank_acc', 'غير محدد')}

        ========================================

        """
