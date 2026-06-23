from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    content = Column(Text, nullable=False)

    source = Column(String, nullable=False)

    url = Column(String, nullable=False)

    published_at = Column(DateTime, nullable=False)