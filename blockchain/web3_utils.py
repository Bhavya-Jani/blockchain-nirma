from web3 import Web3
from django.conf import settings

# Connect to Ethereum Network
web3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))

def get_connection_status():
    """Check connection and return latest block number"""
    if web3.is_connected():
        latest_block = web3.eth.block_number  # Get latest block number
        return f"Connected to Ethereum network. Latest Block: {latest_block}"
    else:
        return "Failed to connect"


ETH_ADDRESS = "" 

def get_eth_balance():
    if web3.is_connected():
        balance_wei = web3.eth.get_balance(ETH_ADDRESS)  # Get balance in Wei
        balance_eth = web3.from_wei(balance_wei, 'ether')  # Convert to ETH
        return f"Connected! ETH Balance of {ETH_ADDRESS}: {balance_eth} ETH"
    else:
        return "Failed to connect"



