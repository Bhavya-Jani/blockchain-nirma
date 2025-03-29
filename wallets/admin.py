from django.contrib import admin
from wallets.models import Wallet
# Register your models here.

class walletadmin(admin.ModelAdmin):
    list_display=('name','password','blockchain_network')

admin.site.register(Wallet,walletadmin)