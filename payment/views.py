from django.shortcuts import render, redirect
import requests
import os
from account.models import Merchant
from Estore.models import Cart
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
"""
# BackUp Payment Code
def pay(request):

    # Merchant Shop Payment
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
            pay_data = {"txref": txt_ref, "amt": fee,
                        "descrip": "Payment for Account Approval"}
            return render(request, 'payment/pay.html', {"merchant": merchant, "pay_data": pay_data})
    else:
        redirect("Mlogin")
    # return render(request, 'payment/pay.html', {})

"""


def pay(request):
    
    # Merchant Shop Payment
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
            pay_data = {"txref": txt_ref, "amt": fee,
                        "descrip": "Payment for Account Approval"}
            return render(request, 'payment/pay.html', {"payer": merchant, "pay_data": pay_data, "type":"shop"})
    else:
        redirect("Mlogin")
    # return render(request, 'payment/pay.html', {})
   
def verify(request):
    mode = request.GET.get('mode', None)
    id = request.GET.get('id', None)
    m = int(id)
    print(m)
    print(verify_transaction(m))

    if mode == "order":
        cust_id = request.session.get('Customer_id', None)
        for cart in Cart.objects.filter(customer_id=cust_id):
            cart.cleared = True
            cart.save()
        print("Cleared Carts")

        return redirect('checkout')
    elif mode == "shop":
        if id is not None:
            
            # get session
            mid = request.session.get('merchant_id', None)

            if mid is not None:
                merchant = Merchant.objects.get(seller_id=mid)
                if verify_transaction(m):
                    merchant.approved = True
                    merchant.save()
        return redirect("Mprofile")

def confirm(request):
    return render(request, 'payment/confirm.html', {})
