from django.http import HttpResponse
from django.shortcuts import render,redirect
from wallets.models import Wallet
from django.contrib.auth.hashers import check_password
from blockchain.web3_utils import get_connection_status
from django.http import JsonResponse
from .utils.solana_utils import get_solana_connection_status, get_latest_solana_block
import requests
from django.conf import settings

def homepage(request):
    return render(request,"index.html")

def aboutus(request):
    return render(request,"aboutus.html")

def signin(request):
    return render(request,"sign_in.html")

def verify_recaptcha(recaptcha_response):
    """Verify reCAPTCHA response with Google's API"""
    secret_key = settings.RECAPTCHA_SECRET_KEY
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": secret_key, "response": recaptcha_response}
    response = requests.post(url, data=payload).json()
    return response.get("success", False)

def try_view(request):
    if request.method == "POST":
        recaptcha_response = request.POST.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            return JsonResponse({"status": "error", "message": "reCAPTCHA verification failed"})

        return JsonResponse({"status": "success", "message": "Human verification successful!"})

    return render(request, "try.html")

def tryhtml(request):
    if request.method == "POST":
        name = request.POST["ename"]
        password = request.POST["epass"]
        blockchain_network = request.POST["blockchain_network"]

        # Check if the wallet with this name already exists
        if Wallet.objects.filter(name=name).exists():
            return render(request, 'index.html', {"error": "Wallet name already exists! Choose a different name."})

        try:
            # Save hashed password in the database
            Wallet.objects.create(name=name, password=password, blockchain_network=blockchain_network)
            return render(request, 'try.html')  # Redirect to success page
        except IntegrityError:
            return render(request, 'index.html', {"error": "Something went wrong! Please try again."})

    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":
        name = request.POST["ename"]
        password = request.POST["epass"]

        try:
            # Fetch the first wallet that matches the name (if multiple exist)
            user = Wallet.objects.filter(name=name).first()

            if user and check_password(password, user.password):
                return render(request, 'login.html', {"user": user})  # Redirect to dashboard
            else:
                return render(request, 'login.html', {"error": "Invalid username or password!"})
        except Exception as e:
            return render(request, 'login.html', {"error": str(e)})

    return render(request, 'login.html')  # Render login page

def blockchain_status(request):
    status = get_connection_status()
    return render(request, 'status.html', {'status': status})

def solana_status_view(request):
    """Django view to check Solana network status"""
    status = get_solana_connection_status()
    return JsonResponse({"status": status})

def solana_latest_block_view(request):
    """Django view to get the latest Solana block (slot number)"""
    latest_block = get_latest_solana_block()
    
    if isinstance(latest_block, int):  # Ensure it's an integer before returning JSON
        return JsonResponse({"latest_block": latest_block})
    else:
        return JsonResponse({"error": latest_block}, status=500)

def wallet(request):
    return render(request,"wallet.html")

def store_private_key(request):
    """API to store a private key"""
    if request.method == 'POST':
        private_key = request.POST.get('private_key')
        user = request.user  # Assumes the user is authenticated
        wallet = BlockchainWallet.objects.get_or_create(user=user)[0]
        wallet.set_private_key(private_key)
        return JsonResponse({'message': 'Private key stored successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_private_key(request):
    """API to retrieve a private key"""
    if request.method == 'GET':
        user = request.user  # Assumes the user is authenticated
        try:
            wallet = BlockchainWallet.objects.get(user=user)
            private_key = wallet.get_private_key()
            return JsonResponse({'private_key': private_key})
        except BlockchainWallet.DoesNotExist:
            return JsonResponse({'error': 'Wallet not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def info(request):
    return render(request,"info.html")

