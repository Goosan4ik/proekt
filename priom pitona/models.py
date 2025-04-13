from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Category (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    keywords: Mapped[str] = mapped_column(nullable=False)
    chat_id: Mapped[str] = mapped_column(nullable=True)
    default_answer: Mapped[str] = mapped_column(nullable=True)


