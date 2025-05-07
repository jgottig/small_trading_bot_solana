
#2e16bc39-17fa-4787-83d7-50b27bb8cc11

import requests
import time

def obtener_market_cap(contract):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{contract}"
    response = requests.get(url)
    data = response.json()
    
    try:
        market_cap = data["pairs"][0]["fdv"]  # FDV = Fully Diluted Valuation (MarketCap)
        return market_cap
    except (KeyError, IndexError):
        print("Contrato no encontrado o sin liquidez.")
        return None

def monitorear_market_cap(contract):
    while True:
        market_cap = obtener_market_cap(contract)
        if market_cap:
            print(f"MarketCap: ${market_cap:,}")
        else:
            print("Esperando nuevo intento...")
        time.sleep(5)

if __name__ == "__main__":
    contract = "82NGnVgT4HxaU3HJdqVVnJ1KH2hKdDEpEB11bAPTA4eG"  # Contrato de Solana
    monitorear_market_cap(contract)

