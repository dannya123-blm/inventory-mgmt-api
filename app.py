from fastapi import FastAPI, HTTPException, Query
from database import products_collection
from models import Product
import requests

app = FastAPI(title="Inventory Management API")

# -----------------------------
# Helper function
# -----------------------------
def product_helper(product):
    return {
        "ProductID": product["ProductID"],
        "Name": product["Name"],
        "UnitPrice": product["UnitPrice"],
        "StockQuantity": product["StockQuantity"],
        "Description": product.get("Description", "")
    }

# -----------------------------
# 1. GET SINGLE PRODUCT
# -----------------------------
@app.get("/getSingleProduct", tags=["Products"])
def get_single_product(
    id: int = Query(..., gt=0, description="Product ID must be > 0")
):
    product = products_collection.find_one({"ProductID": id})
    if product:
        return product_helper(product)
    raise HTTPException(status_code=404, detail="Product not found")


# -----------------------------
# 2. GET ALL PRODUCTS
# -----------------------------
@app.get("/getAll", tags=["Products"])
def get_all():
    products = products_collection.find()
    return [product_helper(p) for p in products]


# -----------------------------
# 3. ADD NEW PRODUCT
# -----------------------------
@app.post("/addNew", tags=["Products"])
def add_new(product: Product):
    existing = products_collection.find_one({"ProductID": product.ProductID})
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    products_collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


# -----------------------------
# 4. DELETE PRODUCT
# -----------------------------
@app.delete("/deleteOne", tags=["Products"])
def delete_one(
    id: int = Query(..., gt=0, description="Product ID must be > 0")
):
    result = products_collection.delete_one({"ProductID": id})
    if result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")


# -----------------------------
# 5. STARTS WITH LETTER
# -----------------------------
@app.get("/startsWith", tags=["Products"])
def starts_with(
    letter: str = Query(..., min_length=1, max_length=1, description="Single letter")
):
    results = products_collection.find({
        "Name": {"$regex": f"^{letter}", "$options": "i"}
    })
    return [product_helper(p) for p in results]


# -----------------------------
# 6. PAGINATE (batch of 10)
# -----------------------------
@app.get("/paginate", tags=["Products"])
def paginate(
    start_id: int = Query(..., gt=0),
    end_id: int = Query(..., gt=0)
):
    if start_id > end_id:
        raise HTTPException(status_code=400, detail="start_id must be <= end_id")

    results = products_collection.find({
        "ProductID": {"$gte": start_id, "$lte": end_id}
    }).sort("ProductID", 1).limit(10)

    return [product_helper(p) for p in results]


# -----------------------------
# 7. CONVERT USD → EUR
# -----------------------------
@app.get("/convert", tags=["Products"])
def convert_price(
    id: int = Query(..., gt=0)
):
    product = products_collection.find_one({"ProductID": id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        if response.status_code != 200:
            raise Exception("API error")

        data = response.json()
        eur_rate = data["rates"]["EUR"]

    except Exception:
        raise HTTPException(status_code=500, detail="Currency API unavailable")

    converted_price = product["UnitPrice"] * eur_rate

    return {
        "ProductID": id,
        "PriceUSD": product["UnitPrice"],
        "PriceEUR": round(converted_price, 2)
    }