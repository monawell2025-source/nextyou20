import pandas as pd
from pathlib import Path
from datetime import datetime

EXCEL_FILE = Path("nextyou_content_bank.xlsx")

def save_to_excel(idea: str, content: str):
    data = {
        "تاریخ": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "ایده": [idea],
        "محتوا": [content]
    }
    df_new = pd.DataFrame(data)

    if EXCEL_FILE.exists():
        df_old = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(EXCEL_FILE, index=False)