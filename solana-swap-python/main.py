import requests
import time
import asyncio
from solders.keypair import Keypair
from solanatracker import SolanaTracker


##################
##################
##################
##################         FUNCION DE OBTENER MARKET CAP
##################
##################
##################


# 🔹 CONFIGURAR TU BILLETERA Y TOKEN
WALLET_ADDRESS = "3Uu8YY1tnyMAnVWCByRvYXNCPWyU44FBiaLVAmMDyBfN"  # Dirección pública de tu billetera# Dirección del token en Solana
RPC_URL = "https://api.mainnet-beta.solana.com"  # RPC de Solana

def get_token_balance(wallet_address, token_mint):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {"mint": token_mint},
            {"encoding": "jsonParsed"}
        ]
    }

    response = requests.post(RPC_URL, json=payload).json()

    try:
        balance = response["result"]["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
        return balance
    except (IndexError, KeyError):
        return "No tienes saldo de este token."





##################
##################
##################
##################         FUNCION DE OBTENER MARKET CAP
##################
##################
##################


# Función para obtener el Market Cap
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

# Función para monitorear el Market Cap
def monitorear_market_cap(contract):
    while True:
        market_cap = obtener_market_cap(contract)
        if market_cap:
            print(f"MarketCap: ${market_cap:,}")
        else:
            print("Esperando nuevo intento...")
        time.sleep(5)
        return market_cap


##################
##################
##################
##################         FUNCION DE COMPRA
##################
##################
##################


# Función para realizar el Swap
async def swap(contratado):
    start_time = time.time()

    # Solicitar el token desde la consola
    contrato_token = contratado #input("Ingresa el contrato del token a comprar: ").strip()

    # Contrato de SOL
    contrato_sol = "So11111111111111111111111111111111111111112"

    keypair = Keypair.from_base58_string("4C9huN5SDZ7cL46mVoCsAsq1xppSvYnHsVbK4jVqcp5eMKZFD8q7nFn9b2CGAcqL3tqMkHN3Vyu2dGX7GNUa1LnC")  # Reemplazar con tu clave privada en base58

    solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")

    # Realizar el swap
    swap_response = await solana_tracker.get_swap_instructions(
        contrato_sol,  # De Token (SOL)
        contrato_token,  # A Token (el que ingrese el usuario)
        0.001,  # Cantidad a intercambiar
        30,  # Slippage
        str(keypair.pubkey()),  # Clave pública del pagador
        0.00005,  # Prioridad de tarifa (Recomendada cuando la red está congestionada)
    )

    # Definir opciones personalizadas
    custom_options = {
        "send_options": {"skip_preflight": True, "max_retries": 5},
        "confirmation_retries": 50,
        "confirmation_retry_timeout": 1000,
        "last_valid_block_height_buffer": 200,
        "commitment": "processed",
        "resend_interval": 1500,
        "confirmation_check_interval": 100,
        "skip_confirmation_check": False,
    }

    try:
        send_time = time.time()
        txid = await solana_tracker.perform_swap(swap_response, options=custom_options)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://solscan.io/tx/{txid}")
        print(f"Swap completed in {elapsed_time:.2f} seconds")
        print(f"Transaction finished in {end_time - send_time:.2f} seconds")
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Swap failed:", str(e))
        print(f"Time elapsed before failure: {elapsed_time:.2f} seconds")



##################
##################
##################
##################         FUNCION DE VENTA
##################
##################
##################

async def swap_venta(contratado, balance):
    start_time = time.time()

    # Solicitar el token desde la consola
    contrato_token = contratado #input("Ingresa el contrato del token a comprar: ").strip()

    # Contrato de SOL
    contrato_sol = "So11111111111111111111111111111111111111112"

    keypair = Keypair.from_base58_string("4C9huN5SDZ7cL46mVoCsAsq1xppSvYnHsVbK4jVqcp5eMKZFD8q7nFn9b2CGAcqL3tqMkHN3Vyu2dGX7GNUa1LnC")  # Reemplazar con tu clave privada en base58

    solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")

    # Realizar el swap
    swap_response = await solana_tracker.get_swap_instructions(
        contrato_token,  # De Token (SOL)
        contrato_sol,  # A Token (el que ingrese el usuario)
        balance,  # Cantidad a intercambiar
        30,  # Slippage
        str(keypair.pubkey()),  # Clave pública del pagador
        0.00005,  # Prioridad de tarifa (Recomendada cuando la red está congestionada)
    )

    # Definir opciones personalizadas
    custom_options = {
        "send_options": {"skip_preflight": True, "max_retries": 5},
        "confirmation_retries": 50,
        "confirmation_retry_timeout": 1000,
        "last_valid_block_height_buffer": 200,
        "commitment": "processed",
        "resend_interval": 1500,
        "confirmation_check_interval": 100,
        "skip_confirmation_check": False,
    }

    try:
        send_time = time.time()
        txid = await solana_tracker.perform_swap(swap_response, options=custom_options)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://solscan.io/tx/{txid}")
        print(f"Swap completed in {elapsed_time:.2f} seconds")
        print(f"Transaction finished in {end_time - send_time:.2f} seconds")
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Swap failed:", str(e))
        print(f"Time elapsed before failure: {elapsed_time:.2f} seconds")






# Función principal que ejecuta el monitoreo y el swap
def main():
    # Solicitar el token desde la consola y realizar el swap
    contrato_token = input("Ingresa el contrato del token a comprar: ").strip()
    
    TOKEN_MINT = contrato_token

    # Realizar el Swap de 0.001 SOL
    asyncio.run(swap(contratado=contrato_token))

    # 🔹 Obtener el saldo del token
    balance = get_token_balance(WALLET_ADDRESS, TOKEN_MINT)
    print(f"Balance del token: {balance}")

    # Iniciar el monitoreo del Market Cap
    print("Monitoreando el Market Cap...")
    market = monitorear_market_cap(contrato_token)
    market_cap_inicial = obtener_market_cap(contrato_token)
    techo_cuarenta = market_cap_inicial * 1.4
    piso_veinte = market_cap_inicial * 0.8
    while True:
        market = monitorear_market_cap(contrato_token)
        balance = get_token_balance(WALLET_ADDRESS, TOKEN_MINT)
        print(f"Balance del token: {balance}")
        if market > techo_cuarenta or market < piso_veinte:
            asyncio.run(swap_venta(contratado = contrato_token, balance= balance))


if __name__ == "__main__":
    main()
