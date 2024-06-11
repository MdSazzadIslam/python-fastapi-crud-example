from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from aioredis import Redis

from src.schemas.product_schema import ProductSchema, UpdateProductSchema
from src.crud.product_crud import (
    get_all,
    get_by_id,
    insert_product,
    update_product,
    delete_product,
)
from src.utils.cache import get_cache, set_cache


async def get_all_products(redis: Redis, db: Session, page: int, page_size: int):
    cache_key = "all_products"

    # Check cache first
    cached_value = await get_cache(redis, cache_key)
    if cached_value:
        return [ProductSchema.parse_obj(product) for product in cached_value]

    skip = (page - 1) * page_size
    limit = page_size

    products = await get_all(db, skip, limit)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No products found"
        )

    # Convert products to Pydantic schemas
    products_list = [ProductSchema.from_orm(product).dict() for product in products]

    await set_cache(redis, cache_key, products_list, expire=300)

    return products


async def get_product_by_id(product_id: UUID, redis: Redis, db: Session):
    cached_product = await get_cache(redis, str(product_id))
    if cached_product:
        # If the product is found in cache, return it
        return cached_product

    product = await get_by_id(product_id, db)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )

    # Convert the Product object to a dictionary using Pydantic's parse_obj_as method
    product_dict = {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        # Add other fields as needed
    }
    # Cache the fetched product for future use
    await set_cache(redis, str(product_id), product_dict)

    return product


async def create_new_product(product: ProductSchema, db: Session):
    return await insert_product(product, db)


async def modify_product(product: UpdateProductSchema, db: Session):
    updated_product = await update_product(product, db)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product.id} not found",
        )
    return updated_product


async def remove_product(product_id: UUID, db: Session):
    deletion_response = await delete_product(product_id, db)
    if not deletion_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )
    return deletion_response
