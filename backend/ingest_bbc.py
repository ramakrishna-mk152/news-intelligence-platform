import feedparser
from datetime import datetime, timezone

from database import SessionLocal
from models import Article

FEED_URL = "https://feeds.bbci.co.uk/news/rss.xml"




def parse_published(entry):
    """Return a naive UTC datetime. Falls back to 'now' if the feed has no date,
    because your published_at column is NOT NULL and can't accept None."""
    if entry.get("published_parsed"):
        # struct_time is already UTC; build a naive datetime to match your column
        return datetime(*entry.published_parsed[:6])
    return datetime.now(timezone.utc).replace(tzinfo=None)


def main():
    feed = feedparser.parse(FEED_URL)
    print(f"Fetched {len(feed.entries)} articles from the feed.")

    db = SessionLocal()
    try:
        added = 0
        for entry in feed.entries[:5]:
            url = entry.get("link")
            title = entry.get("title", "No title")
            # RSS gives a summary, not full text — that's what goes in 'content'
            content = entry.get("summary") or title

            if not url:
                print("Skipping an entry with no URL.")
                continue

            # Duplicate check (your url column isn't UNIQUE, so the app enforces it)
            existing = db.query(Article).filter(Article.url == url).first()
            if existing:
                print(f"Already in DB, skipping: {title}")
                continue

            article = Article(
                title=title,
                content=content,
                source="BBC",
                url=url,
                published_at=parse_published(entry),
            )
            db.add(article)
            added += 1
            print(f"Staged: {title}")

        db.commit()
        print(f"\nDone. {added} new article(s) saved.")
    finally:
        db.close()


if __name__ == "__main__":
    main()