import os
import time
import pandas as pd
import telebot
from telebot import apihelper
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from infrastructure.storage.database import DatabaseManager  # وارد کردن DatabaseManager

# وارد کردن تنظیمات و دیتابیس از فایل‌هایی که قبلاً ساختیم
from config.settings import settings

# تنظیمات شبکه و پروکسی
apihelper.proxy = {'https': settings.PROXY_URL}
apihelper.CONNECT_TIMEOUT = 90
apihelper.READ_TIMEOUT = 90

# راه‌اندازی ربات و دیتابیس
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
db = DatabaseManager()  # ایجاد شی از DatabaseManager
EXCEL_FILE = Path(os.getcwd()) / "nextyou_content_bank.xlsx"

# مدیریت دیتابیس اکسل
def save_to_excel(idea, content):
    new_data = {
        "تاریخ": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "موضوع/ایده": [idea],
        "محتوا": [content]
    }
    df_new = pd.DataFrame(new_data)
    try:
        if EXCEL_FILE.exists():
            df_old = pd.read_excel(EXCEL_FILE)
            pd.concat([df_old, df_new], ignore_index=True).to_excel(EXCEL_FILE, index=False)
        else:
            df_new.to_excel(EXCEL_FILE, index=False)
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره اکسل: {e}")
        return False

# موتور هوش مصنوعی با قابلیت جابجایی (Fallback)
def get_ai_response(prompt):
    # تلاش اول: Groq (بسیار سریع)
    try:
        client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=settings.GROQ_API_KEY)
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            timeout=20
        )
        return res.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Groq خطا داشت، سوئیچ روی OpenRouter... {e}")

    # تلاش دوم: OpenRouter (مدل Gemini Free)
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=settings.OPENROUTER_API_KEY)
        res = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[{"role": "user", "content": prompt}],
            timeout=20
        )
        return res.choices[0].message.content
    except:
        return "❌ خطا: هوش مصنوعی در دسترس نیست. لطفاً وضعیت اتصال و پروکسی را بررسی کنید."

# هندلرهای ربات
@bot.message_handler(commands=['start'])
def welcome(message):
    # ذخیره در دیتابیس اصلی (SQL)
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    bot.reply_to(message, "🚀 به سیستم هوشمند NEXTYOU خوش آمدید!\nموضوع خود را بفرستید تا محتوا تولید شود.")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    bot.send_chat_action(message.chat.id, 'typing')
    answer = get_ai_response(message.text)
    
    if save_to_excel(message.text, answer):
        status = "✅ در اکسل ذخیره شد."
    else:
        status = "⚠️ خطای ذخیره اکسل."
        
    bot.reply_to(message, f"{status}\n\n🤖 پاسخ:\n{answer}")

# اجرای چرخه پایداری ربات
def run_bot():
    print(f"🟢 ربات @nextyou20_bot فعال شد.")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"♻️ تلاش مجدد... {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()