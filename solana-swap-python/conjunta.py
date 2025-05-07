from telethon import TelegramClient, events
import re

# Configura tus credenciales de Telegram
API_ID = "25785550"  # Reemplaza con tu API ID
API_HASH = "5078f1eade419b020f776a0b420bc21c"  # Reemplaza con tu API HASH
CHANNEL_USERNAME = "ouvaiouhashacalls"  # Puede ser el @ del canal o su ID (-100...)

# Inicializa el cliente de Telegram
client = TelegramClient("session_name", API_ID, API_HASH)

# Maneja los nuevos mensajes del canal
@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    message_text = event.message.text
    
    # Expresión regular para extraer el marketcap
    marketcap_pattern = r'\$(\d+\.?\d*[KMB]?) mc'
    marketcap_match = re.search(marketcap_pattern, message_text)
    
    # Expresión regular para extraer el contrato
    contract_pattern = r'([A-Za-z0-9]{44})'
    contract_match = re.search(contract_pattern, message_text)
    
    if marketcap_match and contract_match:
        marketcap = marketcap_match.group(1)
        contract = contract_match.group(1)
        
        print(f"MarketCap: {marketcap}")
        print(f"Contrato: {contract}")
        
        # Aquí puedes usar las variables marketcap y contract para lo que necesites
        # Por ejemplo, guardarlas en una base de datos, enviarlas a otra función, etc.
        
    else:
        print("No se encontró el marketcap o el contrato en el mensaje.")

# Ejecuta el cliente en un bucle infinito
async def main():
    print(f"Escuchando mensajes en {CHANNEL_USERNAME}...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())


