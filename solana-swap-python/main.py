import requests
import time
import asyncio
import re
from telethon import TelegramClient, events
from solders.keypair import Keypair
from solanatracker import SolanaTracker
import pytz
from datetime import datetime


# Set Up Telegram Credentials
API_ID = "#YourApiID"
API_HASH = "#YourAPIHASHTELEGRAM"
CHANNEL_USERNAME = "#ChanellExample123"

# Set Up Solana Credentials
WALLET_ADDRESS = "#YourWalletAddresSolana"
RPC_URL = "https://api.mainnet-beta.solana.com"
KEYPAIR = Keypair.from_base58_string("#PUT HERE KEY PAR AFTER DECODE IN BASE 58")
SOLANA_TRACKER = SolanaTracker(KEYPAIR, "https://rpc.solanatracker.io/public?advancedTx=true")

# Start Client Telegram
client = TelegramClient("session_name", API_ID, API_HASH)

#Function to get actual market cap from contract
def obtener_market_cap(contract):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{contract}"
    response = requests.get(url)
    data = response.json()
    try:
        return data["pairs"][0]["fdv"]
    except (KeyError, IndexError):
        return None

#Function to get actual Balance in Solana Wallet
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

#Funciton to Swap
async def swap(contrato_token, cantidad=0.08):  
    swap_response = await SOLANA_TRACKER.get_swap_instructions(
        "So11111111111111111111111111111111111111112", contrato_token, cantidad, 30, str(KEYPAIR.pubkey()), 0.00005)
    return await SOLANA_TRACKER.perform_swap(swap_response)

#Inverse Swap (sell)
async def swap_venta(contrato_token, balance):
    swap_response = await SOLANA_TRACKER.get_swap_instructions(
        contrato_token, "So11111111111111111111111111111111111111112", balance, 30, str(KEYPAIR.pubkey()), 0.00005)
    return await SOLANA_TRACKER.perform_swap(swap_response)

#Swap to get MC and Contract Addres from Message in Telegram
def extract_market_cap_and_ca(message):
    # Omitimos el filtro inicial, a menos que lo necesites.
    if "JUST MADE" in message:
        return "M", None

    # Sreach MCAP 
    mcap_match = re.search(r"(?:MCAP|Market Cap):\s*(\d+(?:\.\d+)?[KMB]?)", message, re.IGNORECASE)

    # Sreach el CA
    ca_match = re.search(r"CA:\s*`?([A-Za-z0-9]+)`?", message)
    
    # Return MC and CA 
    return (mcap_match.group(1) if mcap_match else "NOKK",
            ca_match.group(1) if ca_match else None)

@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    message_text = event.message.text
    market_cap, contract_address = extract_market_cap_and_ca(message_text)
    message_date_utc = event.message.date  # Esto devuelve un objeto datetime en UTC
    local_timezone = pytz.timezone("America/Argentina/Buenos_Aires")
    message_date_local = message_date_utc.astimezone(local_timezone)
    current_time_local = datetime.now(local_timezone)
    time_difference_seconds = int((current_time_local - message_date_local).total_seconds())
    
    print (message_text)
    print(market_cap)
    print(contract_address)
    print("SENT AGO SECONDS : +++ " + str(time_difference_seconds))

    if time_difference_seconds < 150 and len(market_cap) < 4 and "M" not in market_cap and contract_address:
        print(f"New Token Detected: {contract_address} with MCAP: {market_cap}")
        
        # BUY
        txid_compra = await swap(contract_address)
        print(f"Buy Success: https://solscan.io/tx/{txid_compra}")
        
        # Keep Alert MC with a comparison between Inicial and Actual MC
        market_cap_inicial = obtener_market_cap(contract_address)
        techo = market_cap_inicial * 1.3
        piso = market_cap_inicial * 0.65
        print("el MCI es: " + str(market_cap_inicial))
        print("el TECHO es: " + str(techo))
        print("el PISO es: " + str(piso))
        
        

        ronda = 0 
        while True:
            market = obtener_market_cap(contract_address)
            balance = int(get_token_balance(WALLET_ADDRESS, contract_address))
            print(f"Market Cap now: {market}, Balance: {balance}")
            
            if market > techo:
                ronda = ronda + 1
                balance = balance
                piso = techo * 0.85 #REFRESH TAKE PROFIT AND STOP LOSS PERCENTAGE
                techo = techo * 1.15
                print("NUEVO TECHO ES : " + str(techo))
                print("NUEVO PISO ES : " + str(piso))
                #while balance == 0:
                #    print("Esperando Balance")
                #    balance = get_token_balance(WALLET_ADDRESS, contract_address)
                #    print(f"Market Cap actual: {market}, Balance: {balance}")
                #print("VENTA EN GANANCIA")
                #txid_venta = await swap_venta(contract_address, balance)
                #print(f"Venta realizada: https://solscan.io/tx/{txid_venta}")
                #break
                #Deprecated
            if market < piso:
                balance = balance
                while balance == 0:
                    print("Esperando Balance")
                    balance = int(get_token_balance(WALLET_ADDRESS, contract_address))
                    print(f"Market Cap actual: {market}, Balance: {balance}")
                print("VENTA EN PERDIDA en RONDA " + str(ronda))
                txid_venta = await swap_venta(contract_address, balance)
                print(f"Venta realizada: https://solscan.io/tx/{txid_venta}")
                break
            time.sleep(4)

async def main():
    print(f"Listening messages in {CHANNEL_USERNAME}...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
