import os
from dotenv import load_dotenv

# لود کردن فایل .env از ریشه پروژه
load_dotenv()


class Settings:
    # 1️⃣ توکن ربات تلگرام
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # 2️⃣ کلیدهای هوش مصنوعی
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # 3️⃣ تنظیمات جانبی
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    PROXY_URL = os.getenv("PROXY_URL")
    ENV = os.getenv("ENV", "development")

    @classmethod
    def validate(cls):
        """اعتبارسنجی تنظیمات حیاتی"""
        errors = []

        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN missing in .env")

        if not (cls.GROQ_API_KEY or cls.OPENROUTER_API_KEY):
            errors.append("No AI API key provided (Groq or OpenRouter)")

        if errors:
            raise RuntimeError("❌ Config error:\n" + "\n".join(errors))

        print("✅ Settings validated successfully!")


# نمونه سراسری تنظیمات
settings = Settings()
settings.validate()
