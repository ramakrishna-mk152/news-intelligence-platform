import chromadb
from sentence_transformers import SentenceTransformer



CHROMA_PATH = "./chroma_db"


client = chromadb.PersistentClient(path=CHROMA_PATH)


collection = client.get_or_create_collection(name="news_articles")


model = SentenceTransformer("all-MiniLM-L6-v2")


def add_article(article_id, text):
    """Embed one article's text and store its vector in Chroma under article_id."""
  
    embedding = model.encode(text).tolist()

    
    collection.upsert(
        ids=[str(article_id)],
        embeddings=[embedding],
        documents=[text],
    )


def search_articles(query, top_k=5):
    """Embed the query and return the top_k most semantically similar articles."""
   
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    distances = results["distances"][0]


    matches = []
    SIMILARITY_THRESHOLD = 1.30

    for article_id, document, distance in zip(ids, documents, distances):

        if distance > SIMILARITY_THRESHOLD:
            continue

        matches.append({
            "article_id": int(article_id),
            "text": document,
            "distance": distance,
        })
    return matches