from django.shortcuts import render, redirect
import os
from pathlib import Path
import json
from django.contrib import messages
from time import time
from .models import Merchant
from Estore.models import Store_Category



# load the dictionary data into a variable which becomes a dictionary (type(data)).

data_DIR = Path(__file__).resolve().parent.parent
data_Path = os.path.join(os.path.join(data_DIR, "static"), "data.json")


# Working with Json data
with open(data_Path) as file:
    data = json.loads(file.read())

    #print(data.keys())
    products = data['Product_tb']
   

    # print(categories)
    #print(products)



# Create your views here.

# Merchant's Login 
def Mlogin(request):
    # next = request.GET.get('next')
    if request.method == 'POST':
        email = request.POST['memail']
        password = request.POST['mpassword']

        if Merchant.objects.filter(email=email).exists():
            # create session for login Merchant
            merchant = Merchant.objects.get(email=email)
            request.session.get('merchant_id', '')


            if password == merchant.password:
                
                request.session['merchant_id'] = merchant.seller_id

                return redirect("Mprofile")
            else:
                return redirect("Mlogin")
            #print(merchant.seller_id)
        else:
            return redirect("Mlogin")
    else:
        # delete Merchant session
        try:
            del request.session['merchant_id']
        except KeyError:
            pass
        return render(request, 'accounts/login.html', {})

    
    

# Merchant's Profile 
def Mprofile(request):
    # get session
    id = request.session.get('merchant_id', None)
    # print(id)
    # If session is None, Go and Login
    if id is not None:
        merchant = Merchant.objects.get(seller_id=id)
        merchant_stores = Store_Category.objects.filter(merchant_id=merchant.id)
        # print(merchant_stores)
        return render(request, 'accounts/profile.html', {"products": products.values(), "merchant": merchant, "stores":merchant_stores})
    else:
        return redirect("Mlogin")

def Mlogout(request):
    # delete Merchant session
    try:
        del request.session['merchant_id']
        print("Session Deleted")
    except KeyError:
        pass
    return redirect("Mlogin")

# Merchant's Registration
def Mregister(request):
    if request.method == 'POST':
        name = request.POST['BusiName']
        sellerId = int(str(int(time())*len(name))[:10])
        owner = request.POST['oName']
        phone_number = request.POST['pNumber']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        about = request.POST['aboutBusi']
        industry = request.POST['industry']
        address = request.POST['addrBusi']

        accNum = request.POST['accNumber']
        accName = request.POST['accName']
        country = request.POST['country']
        bank = request.POST['bankName']
        bvn = request.POST['bvn']

        # print(locals())

        
        if password == cpassword:
            if Merchant.objects.filter(email=email).exists():
                print("Email already Exist")
                return redirect("Mregister")
            else:
                new_seller = Merchant(
                                merchant_name = name,
                                seller_id = sellerId,
                                owner = owner,
                                phone_number = phone_number,
                                email = email,
                                password = password,
                                details = about,
                                address = address,
                                industry = industry,
                                acc_no = accNum,
                                acc_name = accName,
                                country = country,
                                bank = bank,
                                bvn = bvn
                                )
                new_seller.save()
                return redirect("Mlogin")
        else:
            print("Password Does not match")
            return redirect("Mregister")
    
    else:
        # If Request is GET
        return render(request, 'accounts/register.html', {})


def addProduct(request):
    return render(request, 'addProd.html', {})


def addStore(request):

    # get session
    id = request.session.get('merchant_id', None)

   
    # print(id)
    # If session is None, Go and Login
    if id is not None:
        merchant = Merchant.objects.get(seller_id=id)
        if request.method == 'POST':
            store_name = request.POST['sName']
            descrip = request.POST['sdescrip']
            industry = request.POST['sindustry']

            # Save Data to DB
            new_store = Store_Category(name=store_name,
                                        merchant_id=merchant,
                                       description=descrip,
                                       industry=industry)
            new_store.save()
            return redirect("Mprofile")
        else:
            return render(request, 'addStore.html', {"owner": merchant})
    else:
        return redirect("Mlogin")
