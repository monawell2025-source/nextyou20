import arxiv

def search_articles(topic, limit=3):
    print(f"Searching for: {topic}...")
    
    # تنظیمات جستجو
    client = arxiv.Client()
    search = arxiv.Search(
        query = topic,
        max_results = limit,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    results = list(client.results(search))
    
    if not results:
        print("No articles found.")
        return

    for i, result in enumerate(results, 1):
        print(f"\n--- Article {i} ---")
        print(f"Title: {result.title}")
        print(f"Date: {result.published.date()}")
        print(f"Link: {result.pdf_url}")
        print(f"Summary: {result.summary[:200]}...") # نمایش خلاصه کوتاه

# تست برنامه با موضوع هوش مصنوعی
if __name__ == "__main__":
    search_articles("Artificial Intelligence")