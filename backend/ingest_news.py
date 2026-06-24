import feedparser
from datetime import datetime, timezone

from database import SessionLocal
from models import Article
from vector_store import add_article
from newspaper import Article as NewsArticle


def extract_article_text(url):
    """Try to download and parse the full article text from a URL.
    Returns the full text on success, or None if scraping fails or finds nothing.
    The CALLER decides what to do with None (we fall back to the RSS summary)."""
    try:
        article = NewsArticle(url)
        article.download()
        article.parse()
        text = article.text

        
        if text and text.strip():
            return text
        return None
    except Exception:
       
        return None

RSS_FEEDS = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen",
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Hindu": "https://www.thehindu.com/news/feeder/default.rss",
    "Indian Express": "https://indianexpress.com/feed/",
    "India Today": "https://www.indiatoday.in/rss/1206584",
    "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
}

MAX_PER_FEED = 10 



def parse_published(entry):
    """Turn the feed's date into a naive UTC datetime.
    Falls back to 'now' because published_at is NOT NULL and can't be None."""
    if entry.get("published_parsed"):
        return datetime(*entry.published_parsed[:6])
    return datetime.now(timezone.utc).replace(tzinfo=None)


def ingest_feed(db, source, url):
    """Fetch ONE feed and save its new articles. Returns how many were added.
    Takes 'source' as an argument so the source name is stored automatically."""
    feed = feedparser.parse(url)
    print(f"[{source}] fetched {len(feed.entries)} articles")

    added = 0
    for entry in feed.entries[:MAX_PER_FEED]:
        article_url = entry.get("link")
        title = entry.get("title", "No title")

        if not article_url:
            continue

      
        exists = db.query(Article).filter(Article.url == article_url).first()
        if exists:
            continue
        summary = entry.get("summary") or title

        full_text = extract_article_text(article_url)

        content = full_text if full_text else summary

        article = Article(
            title=title,
            content=content,
            source=source,
            url=article_url,
            published_at=parse_published(entry),
        )
        db.add(article)
        db.flush()  

    
        text = f"Title: {article.title}\n\nContent: {article.content}"
        add_article(article.id, text)

        added += 1

    return added


def main():
    db = SessionLocal()
    try:
        total = 0
        for source, url in RSS_FEEDS.items():
            try:
                added = ingest_feed(db, source, url)
                db.commit()                 
                total += added
                print(f"[{source}] saved {added} new article(s)\n")
            except Exception as error:
                db.rollback()               
                print(f"[{source}] FAILED: {error}\n")
        print(f"All done. {total} new article(s) saved across all sources.")
    finally:
        db.close()


if __name__ == "__main__":
    main()