import pandas as pd
from pathlib import Path
from datetime import datetime

# فایل اکسل که اطلاعات در آن ذخیره می‌شود
EXCEL_FILE = Path("nextyou_content_bank.xlsx")

def save_to_excel(idea: str, content: str):
    # ایجاد یک دیکشنری از داده‌ها
    data = {
        "تاریخ": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "ایده": [idea],
        "محتوا": [content]
    }
    
    # ایجاد DataFrame از داده‌های جدید
    df_new = pd.DataFrame(data)

    # بررسی اینکه آیا فایل اکسل قبلاً وجود دارد یا نه
    if EXCEL_FILE.exists():
        # اگر فایل قبلاً وجود دارد، داده‌های جدید را به آن اضافه می‌کنیم
        df_old = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        # اگر فایل وجود ندارد، داده‌های جدید را به عنوان اولین داده‌ها ذخیره می‌کنیم
        df = df_new

    # ذخیره داده‌ها در فایل اکسل
    df.to_excel(EXCEL_FILE, index=False)
