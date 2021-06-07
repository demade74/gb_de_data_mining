from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    MetaData,
    Table,
    DateTime,
    Text
)

Base = declarative_base()


tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    title = Column(String, nullable=False, unique=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("Author", backref="posts")
    tags = relationship("Tag", secondary=tag_post, backref="posts")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    name = Column(String, nullable=False, unique=False)

# homework


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), nullable=False, unique=True)
    name = Column(String(100), nullable=False)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    created_at = Column(DateTime, nullable=False)
    body = Column(Text)
    likes_count = Column(Integer)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"))

    author = relationship("Author", backref="comments")
    post = relationship("Post", backref="comments")

    def __init__(self, **data):
        self.id = data["id"]
        self.parent_id = data["parent_id"]
        self.likes_count = data["likes_count"]
        self.body = data["body"]
        self.created_at = datetime.fromisoformat(data["created_at"])
        self.hidden = data["hidden"]
        self.deep = data["deep"]
        self.time_now = datetime.fromisoformat(data["time_now"])


