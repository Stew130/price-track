from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PriceRecord(BaseModel):
    date: datetime
    price: float
    
    # Metodo per la conversione automatica a JSON
    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        d['date'] = d['date'].isoformat()  # Converte `date` in stringa ISO 8601
        return d

# Modello del prodotto
class Product(BaseModel):
    id: str                    # ID del prodotto (ad es. l'ASIN di Amazon)
    title: str                 # Titolo del prodotto
    url: str                   # URL del prodotto
    price_history: List[PriceRecord]  # Storico dei prezzi
    
    # Metodo per la conversione automatica a JSON
    def dict(self, **kwargs):
        # Converte ogni `PriceRecord` usando il proprio metodo `dict` per serializzare `date`
        d = super().dict(**kwargs)
        d['price_history'] = [record.dict() for record in self.price_history]
        return d
