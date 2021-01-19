from django.shortcuts import render, redirect
import requests
import os
from account.models import Merchant
from getenv import env

# Verify Transaction
def verify_transaction(transaction_id):
    
    # transaction_id = 1839314
    url = 'https://api.flutterwave.com/v3/transactions/{}/verify'.format(
        transaction_id)
    
    r = requests.get(url, headers={'Authorization': 'Bearer %s' % os.getenv('ACCESS_TOKEN')})
    droplets = r.json()
    # print(droplets['data']['status'])

    return droplets['data']['status'] == "successful"

# Create your views here.
def pay(request):
    # get session
    id = request.session.get('merchant_id', None)

    if id is not None:
        merchant = Merchant.objects.get(seller_id=id)
        if merchant.approved:
            return redirect("addstore")
        else:
            # print("Yet to Approve")
            txt_ref = env('APP_NAME') + "-approve-" + str(int(merchant.seller_id)+2)[:10]

            fee = 20
            pay_data = {"txref": txt_ref, "amt": fee}
            return render(request, 'payment/pay.html', {"merchant": merchant, "pay_data": pay_data})
    else:
        redirect("Mlogin")
    # return render(request, 'payment/pay.html', {})

def verify(request):
    mode = request.GET.get('id', None)
    

    if mode is not None:
        m = int(mode)
        print(m)
        print(verify_transaction(m))
        # get session
        id = request.session.get('merchant_id', None)

        if id is not None:
            merchant = Merchant.objects.get(seller_id=id)
            if verify_transaction(m):
                merchant.approved = True
                merchant.save()
    return redirect("Mprofile")

def confirm(request):
    return render(request, 'payment/confirm.html', {})
