from database import SessionLocal
from models import Article
from vector_store import add_article
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def main():
   
    db = SessionLocal()
    try:
        
        articles = db.query(Article).all()
        total = len(articles)
        print(f"Found {total} articles to embed.\n")

        
        for index, article in enumerate(articles, start=1):
            
            text = f"Title: {article.title}\n\nContent: {article.content}"
            chunks = text_splitter.split_text(text)
           
            for chunk_index, chunk in enumerate(chunks):
                add_article(
                    article.id,
                    chunk,
                    chunk_index
                )

           
            print(f"[{index}/{total}] embedded article id={article.id}")

        print(f"\nDone. {total} articles embedded into ChromaDB.")
    finally:
   
        db.close()


if __name__ == "__main__":
    main()