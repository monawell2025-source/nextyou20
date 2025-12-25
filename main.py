import os
import time
import pandas as pd
import telebot
from telebot import apihelper
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# وارد کردن تنظیمات و مدیریت دیتابیس از ساختار پروژه
from config.settings import settings

# --- ۱. تنظیمات شبکه و پروکسی ---
apihelper.proxy = {'https': settings.PROXY_URL}
apihelper.CONNECT_TIMEOUT = 90
apihelper.READ_TIMEOUT = 90

# --- ۲. راه‌اندازی ربات ---
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
EXCEL_FILE = Path(os.getcwd()) / "nextyou_content_bank.xlsx"

# --- ۳. مدیریت دیتابیس اکسل ---
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

# --- ۴. موتور هوش مصنوعی (Fallback Logic) ---
def get_ai_response(prompt):
    providers = [
        {
            "name": "Groq",
            "url": "https://api.groq.com/openai/v1",
            "key": settings.GROQ_API_KEY,
            "model": "llama-3.3-70b-versatile"
        },
        {
            "name": "OpenRouter",
            "url": "https://openrouter.ai/api/v1",
            "key": settings.OPENROUTER_API_KEY,
            "model": "google/gemini-2.0-flash-exp:free"
        }
    ]
    for provider in providers:
        try:
            client = OpenAI(base_url=provider["url"], api_key=provider["key"])
            res = client.chat.completions.create(
                model=provider["model"],
                messages=[{"role": "user", "content": prompt}],
                timeout=25
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"⚠️ تلاش با {provider['name']} ناموفق بود: {e}")
            continue
    return "❌ خطا: تمام سرویس‌های هوش مصنوعی با خطا مواجه شدند."

# --- ۵. هندلرهای ربات تلگرام ---
@bot.message_handler(commands=['start'])
def welcome(message):
    try:
        # وارد کردن DatabaseManager داخل تابع
        from infrastructure.storage.database import DatabaseManager
        db = DatabaseManager()
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    except Exception as e:
        print(f"⚠️ خطا در ثبت کاربر: {e}")
    
    bot.reply_to(message, "🚀 به سیستم محتواساز NEXTYOU خوش آمدید!\nموضوع یا ایده خود را بفرستید.")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    # نمایش وضعیت در حال تایپ
    bot.send_chat_action(message.chat.id, 'typing')
    
    # دریافت پاسخ از AI
    answer = get_ai_response(message.text)
    
    # ذخیره در اکسل
    excel_status = save_to_excel(message.text, answer)
    status_msg = "✅ ذخیره در اکسل انجام شد." if excel_status else "⚠️ خطا در بروزرسانی اکسل."
    
    # ارسال نهایی به کاربر
    bot.reply_to(message, f"{status_msg}\n\n🤖 **پاسخ هوش مصنوعی:**\n\n{answer}", parse_mode="Markdown")

# --- ۶. چرخه پایداری (Polling) ---
def run_bot():
    print(f"🟢 ربات @nextyou20_bot روی دایرکتوری {os.getcwd()} فعال شد.")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"♻️ قطع اتصال رخ داد. تلاش مجدد تا ۵ ثانیه دیگر... \nخطا: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
