from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_wallets(request):
    wallets = [
        {"id": 1, "name": "MetaMask", "network": "Ethereum"},
        {"id": 2, "name": "Phantom", "network": "Solana"},
        {"id": 3, "name": "StarkNet", "network": "StarkNet"},
    ]
    return Response(wallets)
