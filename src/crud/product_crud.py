from uuid import UUID
from sqlalchemy.orm import Session
from src.models.product import Product
from src.schemas.product_schema import (
    ProductSchema,
    UpdateProductSchema,
    DeleteProductResponse,
)


async def get_all(db: Session, skip: int, limit: int):
    return db.query(Product).offset(skip).limit(limit).all()


async def get_by_id(product_id: UUID, db: Session):
    return db.query(Product).filter_by(id=product_id).one()


async def insert_product(product: ProductSchema, db: Session):
    product = Product(name=product.name, description=product.description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


async def update_product(product: UpdateProductSchema, db: Session):
    query = {Product.name: product.name, Product.description: product.description}
    db.query(Product).filter_by(id=product.id).update(query)
    db.commit()
    return db.query(Product).filter_by(id=product.id).one()


async def delete_product(product_id: UUID, db: Session):
    product = db.query(Product).filter_by(id=product_id).all()
    if not product:
        return DeleteProductResponse(detail="Product does not exist")
    db.query(Product).filter_by(id=product_id).delete()
    db.commit()
    return DeleteProductResponse(detail="Product deleted successfully")
