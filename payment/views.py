from django.shortcuts import render, redirect
import requests
import os
from account.models import Merchant


def verify_transaction(transaction_id):
    
    # transaction_id = 1839314
    url = 'https://api.flutterwave.com/v3/transactions/{}/verify'.format(
        transaction_id)
    
    r = requests.get(url, headers={'Authorization': 'Bearer %s' % os.getenv('ACCESS_TOKEN')})
    droplets = r.json()
    # print(droplets['data']['status'])

    return droplets['data']['status']

# Create your views here.
def pay(request):
    # get session
    id = request.session.get('merchant_id', None)

    if id is not None:
        merchant = Merchant.objects.get(seller_id=id)
        if merchant.approved:
            return redirect("addstore")
        else:
            return render(request, 'payment/pay.html', {"merchant": merchant})
    else:
        redirect("Mlogin")

def verify(request):
    mode = request.GET.get('id', None)
    

    if mode is not None:
        m = int(mode)
        print(m)
        print(verify_transaction(m))
    return redirect("Mprofile")

def confirm(request):
    return render(request, 'payment/confirm.html', {})
