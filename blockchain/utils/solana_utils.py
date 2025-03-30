from solana.rpc.api import Client
from django.conf import settings

SOLANA_RPC_URL = settings.SOLANA_RPC_URL  # Ensure this exists in settings.py
solana_client = Client(SOLANA_RPC_URL)

def get_solana_connection_status():
    """Check connection by retrieving latest block hash"""
    try:
        response = solana_client.get_latest_blockhash()  # Fetch latest blockhash
        blockhash = response.value.blockhash  # Correctly access blockhash
        return f"Connected to Solana network. Latest Blockhash: {blockhash}"
    except Exception as e:
        return f"Error connecting to Solana: {str(e)}"

def get_latest_solana_block():
    """Retrieve the latest block (slot number) on Solana"""
    try:
        response = solana_client.get_slot()  # Fetch the latest slot (block number)
        return int(response.value)  # Convert to integer for JSON serialization
    except Exception as e:
        return f"Error retrieving latest block: {str(e)}"