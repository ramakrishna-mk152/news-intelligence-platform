from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ask_news import ask
from database import SessionLocal
from models import Article

app = FastAPI()


@app.get("/")
def home():
    return {"message": "News Intelligence Platform"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuestionRequest(BaseModel):
    question: str

class ArticleOut(BaseModel):
    id: int
    title: str
    source: str
    url: str
    published_at: datetime
    content: str

    class Config:
        from_attributes = True


@app.get("/articles", response_model=list[ArticleOut])
def get_articles(source: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Article)

    if source is not None:
        query = query.filter(Article.source == source)

    articles = (
        query
        .order_by(Article.published_at.desc())
        .limit(20)
        .all()
    )

    return articles


@app.get("/search", response_model=list[ArticleOut])
def search_articles(q: str, db: Session = Depends(get_db)):
    pattern = f"%{q}%"

    articles = (
        db.query(Article)
        .filter(Article.title.ilike(pattern))
        .order_by(Article.published_at.desc())
        .limit(20)
        .all()
    )

    return articles

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = ask(request.question)

    if result is None:
        return {
            "question": request.question,
            "answer": "Failed to generate answer.",
            "sources": []   
        }

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }