from fastapi import FastAPI
from routers import products

app = FastAPI()

# Importiamo il router per le API
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Price Tracker API is running"}



#start uvicorn python -m uvicorn main:app --reload