import os
from dotenv import load_dotenv
from google import genai

from vector_store import search_articles
from database import SessionLocal
from models import Article
from datetime import datetime, timedelta, UTC

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL = "gemini-2.5-flash"


def fetch_articles_by_ids(db, article_ids):
    """Fetch full article rows from Postgres for the given ids,
    keeping them in the SAME order vector search ranked them."""
    
    cutoff = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=7)

    rows = (
        db.query(Article)
        .filter(Article.id.in_(article_ids))
        .filter(Article.published_at >= cutoff)
        .all()
    )


    by_id = {article.id: article for article in rows}


    ordered = [by_id[aid] for aid in article_ids if aid in by_id]
    return ordered


def build_context(articles):
    """Build the prompt context from real Postgres fields,
    including source and URL so the answer can cite them."""
    blocks = []
    for article in articles:
        block = (
            f"[Article {article.id}]\n"
            f"Title: {article.title}\n"
            f"Source: {article.source}\n"
            f"URL: {article.url}\n"
            f"Published: {article.published_at}\n"
            f"Content: {article.content[:6700]}"
        )
        blocks.append(block)
    return "\n\n".join(blocks)


def ask(question):
   
    results = search_articles(question, top_k=10)
    retrieved_ids = [m["article_id"] for m in results]
    print(f"Retrieved article IDs: {retrieved_ids}\n")

    if not retrieved_ids:
        print("No articles found. Did you run embed_articles.py first?")
        return

  
    db = SessionLocal()
    try:
        articles = fetch_articles_by_ids(db, retrieved_ids)
        print("\nRetrieved Articles:\n")

        for match in results:
            print(
                f"id={match['article_id']} "
                f"distance={match['distance']:.4f}"
            )
        if not articles:
            print("Vector search returned ids, but none exist in Postgres.")
            return
        context = build_context(articles)
    finally:
        db.close()

 
    prompt = f"""
You are an intelligent news analyst.

Your job is to answer the user's question using ONLY the provided news articles.

Rules:
1. Synthesize information across articles instead of simply listing article contents.
2. Give a direct answer to the user's question first.
3. If multiple articles discuss the same topic, combine them into a coherent explanation.
4. Use bullet points only when they improve readability.
5. Do NOT mention article IDs.
6. Do NOT invent facts not present in the articles.
7. If the articles do not contain enough information, explicitly say so.
8. At the end, provide sources in the format:
   Source: <source name> - <url>
9. Focus on answering the user's question directly.
10. Mention only the most relevant causes and events.
11. Avoid spending excessive detail on secondary background information.

News Articles:
{context}

User Question:
{question}

Answer:
"""

   
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
    except Exception as error:
        print(f"Gemini call failed: {error}")

        return {
            "answer": f"Gemini is temporarily unavailable: {error}",
            "sources": []
        }

    print("Answer:")
    sources = []

    for article in articles:
        sources.append({
            "title": article.title,
            "source": article.source,
            "url": article.url
        })

    return {
        "answer": response.text,
        "sources": sources
    }


if __name__ == "__main__":
    answer = ask("What happened in AI recently?")
    print(answer)