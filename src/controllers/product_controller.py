from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schemas.product_schema import ProductSchema, UpdateProductSchema
from src.crud.product_crud import get_all, get_by_id, insert_product, update_product, delete_product
from uuid import UUID

async def get_all_products(db: Session):
    products = await get_all(db)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products

async def get_product_by_id(product_id: UUID, db: Session):
    product = await get_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return product

async def create_new_product(product: ProductSchema, db: Session):
    return await insert_product(product, db)

async def modify_product(product: UpdateProductSchema, db: Session):
    updated_product = await update_product(product, db)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product.id} not found")
    return updated_product

async def remove_product(product_id: UUID, db: Session):
    deletion_response = await delete_product(product_id, db)
    if not deletion_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return deletion_response
