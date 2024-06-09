from sqlalchemy import String, Column, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()
class Product(Base):
    __tablename__ = "products"

    id = Column(
        String(255),
        default=uuid4,
        primary_key=True,
        index=True
    )
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default= text('Now()'), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default= text('Now()'),
        server_onupdate= text('Now()'),
        nullable=False,
    )