from fastapi import APIRouter, HTTPException, Query
from models.product import ProductCreate, ProductOut
from db.mongodb import product_collection
from bson import ObjectId
from typing import List, Optional

router = APIRouter()

@router.post("/", status_code=201)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    result = await product_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@router.get("/", response_model=dict)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = Query(10),
    offset: int = Query(0)
):
    filters = {}
    if name:
        filters["name"] = {"$regex": name, "$options": "i"}
    if size:
        filters["sizes.size"] = size

    cursor = product_collection.find(filters).skip(offset).limit(limit)
    products = []
    async for product in cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
        })

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": max(0, offset - limit)
        }
    }
