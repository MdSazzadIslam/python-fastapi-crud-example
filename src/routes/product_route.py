from typing import List, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.schemas.product_schema import ProductSchema, UpdateProductSchema, DeleteProductResponse
from src.controllers.product_controller import (
    get_all_products, get_product_by_id, create_new_product, modify_product, remove_product
)
from uuid import UUID

router = APIRouter(tags=['products'])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)) -> List[ProductSchema]:
    return get_all_products(db=db)

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductSchema)
def get_product(product_id:UUID, db: Session = Depends(get_db)) -> Union[ProductSchema, None]:
    return get_product_by_id(product_id, db=db)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db)) -> ProductSchema:
    return create_new_product(product, db=db)

@router.patch("/update", status_code=status.HTTP_200_OK, response_model=UpdateProductSchema)
def update_product(product: UpdateProductSchema, db: Session = Depends(get_db)) -> ProductSchema:
    return modify_product(product, db=db)

@router.delete("/delete/{product_id}", status_code=status.HTTP_200_OK, response_model=DeleteProductResponse)
def delete_product(product_id:UUID, db: Session = Depends(get_db)) -> DeleteProductResponse:
    return remove_product(product_id, db=db)
