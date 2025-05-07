"""import re
mensaje = 🚀 NEW SOL HIGH VOLUME TOKEN 🚀

            🎯 Token Symbol: $PWEPWE
            🛢 MCAP: 110K
            ⏳ Age: 33m
            🌳 Mint: ✅
            🔥 LP Burn: ✅
            🐳 Top 10: 18.71%
            🚨 Risks: Good
            🏟️ CTO?: ❌
            🌐 Socials: [ ](https://dexscreener.com/solana/e7b8eezdpegputzaajt2tsk1qwgs7xbwnr8papdlzwwk)
               [X](https://x.com/PwePweonSOL)
               [Website](https://t.me/pwepweonsol)
               [TG](https://t.me/pwepweonsol)


            📃 CA: `m6NYMnJynzkj7yBwyGJNJBKJsu7TgqiLCwLVvw5pump`

[DEX](https://dexscreener.com/solana/e7b8eezdpegputzaajt2tsk1qwgs7xbwnr8papdlzwwk)  |  [RugCheck](https://rugcheck.xyz/tokens/m6NYMnJynzkj7yBwyGJNJBKJsu7TgqiLCwLVvw5pump)  |  [PF](https://pump.fun/coin/m6NYMnJynzkj7yBwyGJNJBKJsu7TgqiLCwLVvw5pump)  |  [BullxAccess](https://t.me/BullxBetaBot?start=access_H8TLU3OA0P)  |  [TTF](https://t.me/ttfbotbot?start=m6NYMnJynzkj7yBwyGJNJBKJsu7TgqiLCwLVvw5pump)  |  [SOUL](https://t.me/soul_scanner_bot?start=m6NYMnJynzkj7yBwyGJNJBKJsu7TgqiLCwLVvw5pump)       
110K
None

import re

def extract_market_cap_and_ca(message):
    # Omitimos el filtro inicial, a menos que lo necesites.
    if "JUST MADE" in message:
        return None, None

    # Buscamos MCAP con diferentes posibles variaciones
    mcap_match = re.search(r"(?:MCAP|Market Cap):\s*(\d+(?:\.\d+)?[KMB]?)", message, re.IGNORECASE)

    # Buscamos el CA después de "CA:" o "📃 CA:", contenido dentro de backticks o no
    ca_match = re.search(r"CA:\s*`?([A-Za-z0-9]+)`?", message)

    # Devuelve el Market Cap y el Contract Address si los encuentra
    return (mcap_match.group(1) if mcap_match else None,
            ca_match.group(1) if ca_match else None)


x = extract_market_cap_and_ca(mensaje)
print(x)"""

import requests
import time
def obtener_market_cap(contract):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{contract}"
    response = requests.get(url)
    data = response.json()
    #print(data)
    try:
        return data["pairs"][0]["fdv"]
    except (KeyError, IndexError):
        return None
    
while True:
    market = obtener_market_cap("AhJ2u3o7CK4sPk9WQ2rr8FwG1xSTBMMqkjXZbeqapump")
    print(market)
    time.sleep(4)