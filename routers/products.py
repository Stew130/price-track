from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.product import Product, PriceRecord
from services.scraper import get_product_info
import json
from datetime import datetime

router = APIRouter()

# Definisci uno schema di richiesta per il corpo della richiesta
class ProductRequest(BaseModel):
    product_url: str

# Endpoint per aggiungere un nuovo prodotto
@router.post("/add_product/")
async def add_product(request: ProductRequest):
    # Otteniamo il link del prodotto
    product_url = request.product_url
    
    # Eseguiamo lo scraping per ottenere i dettagli del prodotto
    product_data = get_product_info(product_url)
    if product_data:
        # Creiamo una nuova istanza del modello Product
        product = Product(
            id=product_data["id"],
            title=product_data["title"],
            url=product_data["url"],
            price_history=[
                PriceRecord(date=datetime.now(), price=product_data["price"])
            ]
        )
        # Salviamo i dati del prodotto in un file JSON
        with open(f"data/{product.id}.json", "w") as f:
            json.dump(product.dict(), f)
        return {"status": "success", "data": product}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
