from fastapi import APIRouter, HTTPException
from models.order import OrderCreate
from db.mongodb import order_collection, product_collection
from bson import ObjectId
from fastapi import Query
from typing import Optional

router = APIRouter()

@router.post("/", status_code=201)
async def create_order(order: OrderCreate):
    total_order_items = []

    for item in order.items:
        # Validate product
        product = await product_collection.find_one({"_id": ObjectId(item.productId)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.productId} not found.")

        # Check if quantity is available in any size
        size_found = False
        for size in product["sizes"]:
            if size["quantity"] >= item.qty:
                size["quantity"] -= item.qty  # Reduce stock
                size_found = True
                break

        if not size_found:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity for product {item.productId}")

        # Update product stock
        await product_collection.update_one(
            {"_id": ObjectId(item.productId)},
            {"$set": {"sizes": product["sizes"]}}
        )

        total_order_items.append({
            "productId": ObjectId(item.productId),  # Convert to ObjectId here
            "qty": item.qty
        })

    # Create order record
    order_doc = {
        "userId": order.userId,
        "items": total_order_items
    }
    result = await order_collection.insert_one(order_doc)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}", status_code=200)
async def get_orders(user_id: str, limit: int = Query(10), offset: int = Query(0)):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "productDetails"
            }
        }
    ]

    results = []
    async for order in order_collection.aggregate(pipeline):
        items_with_details = []
        total_price = 0.0

        for item in order["items"]:
            # Match the product detail by ID
            prod_detail = next((p for p in order["productDetails"] if str(p["_id"]) == str(item["productId"])), None)
            if prod_detail:
                items_with_details.append({
                    "productDetails": {
                        "name": prod_detail["name"],
                        "id": str(prod_detail["_id"])
                    },
                    "qty": item["qty"]
                })
                total_price += item["qty"] * prod_detail["price"]

        results.append({
            "id": str(order["_id"]),
            "items": items_with_details,
            "total": total_price
        })

    return {
        "data": results,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": max(0, offset - limit)
        }
    }

@router.delete("/clear-orders")
async def clear_orders():
    result = await order_collection.delete_many({})
    return {"deleted_count": result.deleted_count}

@router.get("/inspect-orders")
async def inspect_orders():
    orders = []
    async for doc in order_collection.find({}):
        orders.append(doc)
    return orders