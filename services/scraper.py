import requests
from bs4 import BeautifulSoup

def get_product_info(product_url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    
    # Esegui una richiesta HTTP per ottenere la pagina del prodotto
    response = requests.get(product_url, headers=headers)
    if response.status_code != 200:
        return None  # Errore di connessione

    # Analizza il contenuto HTML della pagina
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Verifica se Amazon ha bloccato la richiesta
    if "captcha" in response.url or (soup.title and "Pagina non disponibile" in soup.title.string):
        return None  # Non siamo riusciti a raggiungere la pagina del prodotto
    
    # Estrai l'ID del prodotto dall'URL
    product_id = product_url.split("/dp/")[1].split("/")[0]
    
    # Estrai il titolo del prodotto
    title = soup.find(id="productTitle")
    if title:
        title = title.get_text(strip=True)
    else:
        title = "Titolo non disponibile"
    
    # Estrai il prezzo del prodotto
    price = None
    price_element = soup.find("span", class_="a-offscreen")
    if not price_element:
        # Prova un'altra classe o struttura
        price_element = soup.find("span", class_="a-price-whole")
        if price_element:
            cents = soup.find("span", class_="a-price-fraction").get_text(strip=True)
            price = f"{price_element.get_text(strip=True)}.{cents}"
            try:
                price = float(price.replace(",", "."))
            except ValueError:
                price = None  # Errore nel parsing del prezzo
    else:
        try:
            price = float(price_element.get_text(strip=True).replace("€", "").replace(",", "."))
        except ValueError:
            price = None  # Errore nel parsing del prezzo

    return {
        "id": product_id,
        "title": title,
        "url": product_url,
        "price": price
    }
