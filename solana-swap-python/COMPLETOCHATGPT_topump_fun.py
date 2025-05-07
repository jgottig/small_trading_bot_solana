import requests
import time
import asyncio
import re
from telethon import TelegramClient, events
from solders.keypair import Keypair
from solanatracker import SolanaTracker

# Configurar credenciales de Telegram
API_ID = "25785550"
API_HASH = "5078f1eade419b020f776a0b420bc21c"
CHANNEL_USERNAME = "solautobot_pumpfunalert"

# Configurar credenciales de Solana
WALLET_ADDRESS = "3Uu8YY1tnyMAnVWCByRvYXNCPWyU44FBiaLVAmMDyBfN"
RPC_URL = "https://api.mainnet-beta.solana.com"
KEYPAIR = Keypair.from_base58_string("4C9huN5SDZ7cL46mVoCsAsq1xppSvYnHsVbK4jVqcp5eMKZFD8q7nFn9b2CGAcqL3tqMkHN3Vyu2dGX7GNUa1LnC")
SOLANA_TRACKER = SolanaTracker(KEYPAIR, "https://rpc.solanatracker.io/public?advancedTx=true")

# Inicializar cliente de Telegram
client = TelegramClient("session_name", API_ID, API_HASH)

def obtener_market_cap(contract):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{contract}"
    response = requests.get(url)
    data = response.json()
    try:
        return data["pairs"][0]["fdv"]
    except (KeyError, IndexError):
        return None

def get_token_balance(wallet_address, token_mint):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [wallet_address, {"mint": token_mint}, {"encoding": "jsonParsed"}]
    }
    response = requests.post(RPC_URL, json=payload).json()
    try:
        return response["result"]["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
    except (IndexError, KeyError):
        return 0

async def swap(contrato_token, cantidad=0.001):
    swap_response = await SOLANA_TRACKER.get_swap_instructions(
        "So11111111111111111111111111111111111111112", contrato_token, cantidad, 30, str(KEYPAIR.pubkey()), 0.00005)
    return await SOLANA_TRACKER.perform_swap(swap_response)

async def swap_venta(contrato_token, balance):
    swap_response = await SOLANA_TRACKER.get_swap_instructions(
        contrato_token, "So11111111111111111111111111111111111111112", balance, 30, str(KEYPAIR.pubkey()), 0.00005)
    return await SOLANA_TRACKER.perform_swap(swap_response)

def extract_market_cap_and_ca(message):
    if "JUST MADE" in message:
        return None, None

    # Expresión regular ajustada para Market Cap
    mcap_match = re.search(r"Market Cap:\s*\*\*\$(\d+(?:\.\d+)?[KMB]?)\*\*", message)

    # Expresión regular ajustada para CA (Contrato)
    ca_match = re.search(r"CA:\s*`([A-Za-z0-9]+)`", message)

    return (mcap_match.group(1) if mcap_match else None, ca_match.group(1) if ca_match else None)


@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    time.sleep(5)
    message_text = event.message.text
    #print(message_text)
    market_cap, contract_address = extract_market_cap_and_ca(message_text)
    print(market_cap)
    print(contract_address)

    if "M" not in market_cap and contract_address:
        print(f"Nuevo token detectado: {contract_address} con MCAP: {market_cap}")
        
        # Realizar compra
        txid_compra = await swap(contract_address)
        print(f"Compra realizada: https://solscan.io/tx/{txid_compra}")
        
        # Monitorear Market Cap y realizar venta si se alcanzan condiciones
        market_cap_inicial = obtener_market_cap(contract_address)
        techo = market_cap_inicial * 1.3
        piso = market_cap_inicial * 0.8
        print("el MKI es: " + str(market_cap_inicial))
        print("el TECHO es: " + str(techo))
        print("el PISO es: " + str(piso))
        
        i = 0 
        while True:
            i = i+1
            if i == 10 and balance == 0:
                break
            market = obtener_market_cap(contract_address)
            balance = int(get_token_balance(WALLET_ADDRESS, contract_address))
            print(f"Market Cap actual: {market}, Balance: {balance}")
            
            if market > techo:
                print("VENTA EN GANANCIA")
                txid_venta = await swap_venta(contract_address, balance)
                print(f"Venta realizada: https://solscan.io/tx/{txid_venta}")
                break
            if market < piso:
                print("VENTA EN PERDIDA")
                txid_venta = await swap_venta(contract_address, balance)
                print(f"Venta realizada: https://solscan.io/tx/{txid_venta}")
                break
            time.sleep(5)

async def main():
    print(f"Escuchando mensajes en {CHANNEL_USERNAME}...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
