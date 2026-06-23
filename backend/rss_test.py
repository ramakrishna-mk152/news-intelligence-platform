import feedparser

FEED_URL = "https://feeds.bbci.co.uk/news/rss.xml"

feed = feedparser.parse(FEED_URL)


if feed.bozo:
    print(f"Warning: feed may be malformed -> {feed.bozo_exception}")

print(f"Feed title: {feed.feed.get('title', 'Unknown')}")
print(f"Total articles in feed: {len(feed.entries)}\n")


for i, entry in enumerate(feed.entries[:5], start=1):
    title = entry.get("title", "No title")
    link = entry.get("link", "No link")
    published = entry.get("published", "No date")

    print(f"--- Article {i} ---")
    print(f"Title:     {title}")
    print(f"Link:      {link}")
    print(f"Published: {published}")
    print()