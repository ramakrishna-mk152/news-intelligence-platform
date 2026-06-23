from newspaper import Article


URL = "https://techcrunch.com/2026/06/22/openai-launches-new-initiative-to-help-find-and-patch-open-source-bugs/"


article = Article(URL)

try:

    article.download()


    article.parse()
except Exception as error:
    print(f"Failed to download or parse the article: {error}")
    raise SystemExit  

print("TITLE:", article.title)
print()


text = article.text
if not text:
    print("No article text was extracted (the page may be paywalled, "
          "JavaScript-rendered, or blocking scrapers).")
else:
    print("TEXT (first 50000 chars):")
    print(text[:50000])