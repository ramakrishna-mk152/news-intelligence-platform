from vector_store import search_articles


QUERY = "What happened in AI recently?"


def main():
    print(f"Query: {QUERY}\n")

    results = search_articles(QUERY, top_k=5)

    if not results:
        print("No results. Did you run embed_articles.py to populate ChromaDB?")
        return

    for rank, match in enumerate(results, start=1):
        distance = match["distance"]
        
        similarity = 1 / (1 + distance)

        print(f"#{rank}  article_id={match['article_id']}")
        print(f"     distance={distance:.4f}   similarity≈{similarity:.4f}")
        print(f"     {match['text'][:100]}...")
        print()


if __name__ == "__main__":
    main()