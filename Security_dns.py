import hashlib
import os
import time

# حدد المجلدات أو الملفات المهمة التي تريد مراقبتها
WATCHED_DIR = "./my_important_files"  # غير هذا المسار إلى المجلد الذي تريد حمايته

def get_file_hash(filepath):
    """حساب البصمة الرقمية (SHA-256) للملف للتأكد من عدم تغييره"""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None

def monitor_files(directory):
    print(f"[*] بدء نظام مراقبة سلامة الملفات في: {directory}")
    print("[*] يتم الآن تسجل البصمات الرقمية للملفات...")

    file_hashes = {}

    # التخزين الأول لبصمات الملفات
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_hashes[full_path] = get_file_hash(full_path)

    print("[✔] تم حفظ البصمات. النظام يعمل الآن ويراقب التغييرات...\n")

    try:
        while True:
            time.sleep(5)  # الفحص كل 5 ثوانٍ
            for root, _, files in os.walk(directory):
                for file in files:
                    full_path = os.path.join(root, file)
                    current_hash = get_file_hash(full_path)

                    if full_path not in file_hashes:
                        print(f"[⚠️ تحذير]: تم إنشاء ملف جديد مجهول: {full_path}")
                        file_hashes[full_path] = current_hash
                    elif file_hashes[full_path] != current_hash:
                        print(f"[🚨 تنبيه أمني]: تم تعديل هذا الملف بشكل مريب! -> {full_path}")
                        file_hashes[full_path] = current_hash

    except KeyboardInterrupt:
        print("\n[*] تم إيقاف نظام المراقبة.")

if __name__ == "__main__":
    if not os.path.exists(WATCHED_DIR):
        os.makedirs(WATCHED_DIR)
    monitor_files(WATCHED_DIR)
