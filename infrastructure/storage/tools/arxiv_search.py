import arxiv

def search_articles(topic: str, limit=3):
    """
    جستجو در مقالات arXiv بر اساس موضوع داده‌شده.
    
    پارامترها:
    - topic: موضوع مورد نظر برای جستجو
    - limit: تعداد نتایج مورد نظر (پیش‌فرض: 3)
    
    خروجی:
    - یک لیست از دیکشنری‌ها که شامل عنوان، تاریخ انتشار و لینک PDF است.
    """
    client = arxiv.Client()
    
    search = arxiv.Search(
        query=topic,  # موضوع جستجو
        max_results=limit,  # حداکثر تعداد نتایج
        sort_by=arxiv.SortCriterion.SubmittedDate  # مرتب‌سازی بر اساس تاریخ ارسال
    )
    
    results = []
    
    # پردازش نتایج جستجو
    for r in client.results(search):
        results.append({
            "title": r.title,
            "date": r.published.date(),
            "url": r.pdf_url  # لینک PDF مقاله
        })

    return results
