import pandas as pd
from datetime import datetime
from pathlib import Path
import os

def test_save():
    # مسیر ذخیره سازی در پوشه فعلی پروژه
    EXCEL_FILE = Path(os.getcwd()) / "test_output.xlsx"
    print(f"📂 در حال تست ذخیره‌سازی در: {EXCEL_FILE}")
    
    test_data = {
        "تاریخ": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "ایده": ["تست محتوای آفلاین"],
        "محتوا": ["این یک متن تستی برای اطمینان از سلامت کتابخانه Pandas است."]
    }
    
    try:
        df = pd.DataFrame(test_data)
        df.to_excel(EXCEL_FILE, index=False)
        print("✅ پیروزی! فایل اکسل با موفقیت ساخته شد.")
        print(f"🚀 فایل را در پوشه پروژه با نام test_output.xlsx چک کنید.")
    except Exception as e:
        print(f"❌ خطا در بخش اکسل: {e}")

if __name__ == "__main__":
    test_save()