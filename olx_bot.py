import asyncio
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# === KONFIGURACJA ===
TELEGRAM_TOKEN = "7967390150:AAGG3wcT1df-RQbxyX-a3e1iANEhvZBsfQ8"  
TELEGRAM_CHAT_ID = "6808256526"  
SLOWA_KLUCZOWE = "iphone"  
LOKALIZACJA = "bialystok"  
CENA_MIN = 100  
CENA_MAX = 2000  
CZAS_ODSWIEZANIA = 60  

# === START BOTA ===
bot = Bot(token=TELEGRAM_TOKEN)
widziane_linki = set()

async def wyslij_na_telegram(oferty):
    for oferta in oferty:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=oferta)

async def szukaj_olx():
    url = f"https://www.olx.pl/oferty/q-{SLOWA_KLUCZOWE}/?search%5Border%5D=created_at:desc&search%5Bfilter_float_price:from%5D={CENA_MIN}&search%5Bfilter_float_price:to%5D={CENA_MAX}&search%5Bcity_id%5D={LOKALIZACJA}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    oferty = soup.select('div[data-cy="l-card"]')

    nowe_oferty = []
    for oferta in oferty:
        link = oferta.find('a')['href']
        tytul = oferta.find('h6')
        if link and tytul and link not in widziane_linki:
            widziane_linki.add(link)
            nowe_oferty.append(f"{tytul.text.strip()}\n{link}")
    return nowe_oferty

async def main():
    # TEST WYSYŁANIA WIADOMOŚCI
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Bot działa i potrafi wysyłać wiadomości!")

    # Główna pętla bota
    while True:
        try:
            oferty = await szukaj_olx()
            if oferty:
                await wyslij_na_telegram(oferty)
            else:
                print("Brak nowych ofert.")
        except Exception as e:
            print(f"Błąd: {e}")
        await asyncio.sleep(CZAS_ODSWIEZANIA)

# Uruchomienie bota
asyncio.run(main())


