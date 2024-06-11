import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
import uuid

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def sqlalchemy_obj_to_dict(obj):
    """Convert SQLAlchemy object to dictionary, converting UUIDs to strings."""
    dict_obj = {}
    for c in class_mapper(obj.__class__).mapped_table.columns:
        value = getattr(obj, c.key)
        if isinstance(value, uuid.UUID):
            value = str(value)
        dict_obj[c.key] = value
    return dict_obj


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
