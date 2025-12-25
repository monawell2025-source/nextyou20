from openai import OpenAI
from config.settings import settings

MODELS = [
    {
        "name": "llama-3.3-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": settings.GROQ_API_KEY,
        "provider": "GROQ"
    },
    {
        "name": "google/gemini-2.0-flash-exp:free",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": settings.OPENROUTER_API_KEY,
        "provider": "OPENROUTER"
    }
]

def generate_text(prompt: str) -> str:
    """
    Unified AI entrypoint with fallback
    """
    for model in MODELS:
        if not model["api_key"]:
            continue

        try:
            client = OpenAI(
                api_key=model["api_key"],
                base_url=model["base_url"]
            )

            response = client.chat.completions.create(
                model=model["name"],
                messages=[{"role": "user", "content": prompt}],
                timeout=30
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️ {model['provider']} failed: {e}")

    return "❌ هیچ مدل هوش مصنوعی در دسترس نیست."
