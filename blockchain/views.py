from django.http import HttpResponse
from django.shortcuts import render,redirect
from wallets.models import Wallet
from django.contrib.auth.hashers import check_password
from blockchain.web3_utils import get_connection_status
from blockchain.web3_utils import get_eth_balance



def homepage(request):
    return render(request,"index.html")

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

def block_status(request):
    status1=get_eth_balance()
    return render(request,'eth_status.html',{'status1':status1})


