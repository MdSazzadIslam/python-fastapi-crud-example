from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID


class HealthResponse(BaseModel):
    status: str


class ProductSchema(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str]
    description: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class UpdateProductSchema(BaseModel):
    id: UUID
    name: Optional[str] = None
    description: Optional[str]


class FilteredProductResponse(ProductSchema):
    id: UUID


class DeleteProductResponse(BaseModel):
    detail: str
