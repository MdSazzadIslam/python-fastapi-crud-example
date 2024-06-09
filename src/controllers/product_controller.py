from typing import List, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schemas.product_schema import ProductSchema, UpdateProductSchema, DeleteProductResponse
from src.crud.product_crud import get_all, get_by_id, insert_product, update_product, delete_product
from uuid import UUID

def get_all_products(db: Session) -> List[ProductSchema]:
    products = get_all(db=db)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products

def get_product_by_id(product_id: UUID, db: Session) -> Union[ProductSchema, None]:
    product = get_by_id(product_id, db=db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return product

def create_new_product(product: ProductSchema, db: Session) -> ProductSchema:
    return insert_product(product=product, db=db)

def modify_product(product: UpdateProductSchema, db: Session) -> ProductSchema:
    updated_product = update_product(product=product, db=db)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product.id} not found")
    return updated_product

def remove_product(product_id: UUID, db: Session) -> DeleteProductResponse:
    deletion_response = delete_product(product_id, db=db)
    if not deletion_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return deletion_response
