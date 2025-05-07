from telethon import TelegramClient, events
import re
from datetime import timezone
from datetime import datetime
import pytz
import pytz

# Configura tus credenciales de Telegram
API_ID = "25785550"  # Reemplaza con tu API ID
API_HASH = "5078f1eade419b020f776a0b420bc21c"  # Reemplaza con tu API HASH
CHANNEL_USERNAME = "QuantumAlphaWeb3"  # Puede ser el @ del canal o su ID (-100...)

# Inicializa el cliente de Telegram
client = TelegramClient("session_name", API_ID, API_HASH)

def extract_market_cap_and_ca(message):
    # Omitir mensaje si contiene "JUST MADE"
    if "JUST MADE" in message:
        return None, None
    
    # Extraer Market Cap
    mcap_match = re.search(r"MCAP:\s*(\d+(?:\.\d+)?[KMB]?)", message)
    market_cap = mcap_match.group(1) if mcap_match else None
    
    # Extraer solo el código del contrato
    ca_match = re.search(r"CA:\s*([A-Za-z0-9]+)", message)
    contract_address = ca_match.group(1) if ca_match else None
    
    return market_cap, contract_address

# Maneja los nuevos mensajes del canal
@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    message_text = event.message.text
    message_date_utc = event.message.date  # Esto devuelve un objeto datetime en UTC
    local_timezone = pytz.timezone("America/Argentina/Buenos_Aires")
    message_date_local = message_date_utc.astimezone(local_timezone)
    current_time_local = datetime.now(local_timezone)
    time_difference_seconds = int((current_time_local - message_date_local).total_seconds())

    print("DIFERENCIA EN SEGUNDOS")
    print(time_difference_seconds)


    market_cap, contract_address = extract_market_cap_and_ca(message_text)
    
    if market_cap and contract_address:
        print(f"\nNuevo mensaje procesado:")
        print(f"Fecha y hora (UTC): {message_date_utc.strftime('%Y-%m-%d %H:%M:%S')}")
        # Si querés mostrar la hora local, descomenta la línea siguiente:
        # print(f"Fecha y hora (Local): {message_date_local.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Market Cap: {market_cap}")
        print(f"Contrato: {contract_address}")
    else:
        print("Mensaje omitido.")

# Ejecuta el cliente en un bucle infinito
async def main():
    print(f"Escuchando mensajes en {CHANNEL_USERNAME}...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
