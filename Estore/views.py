from django.shortcuts import render
from pathlib import Path
import os
import json

# load the dictionary data into a variable which becomes a dictionary (type(data)).

data_DIR = Path(__file__).resolve().parent.parent
data_Path = os.path.join(os.path.join(data_DIR, "static"), "data.json")


# Working with Json data
with open(data_Path) as file:
    data = json.loads(file.read())

    #print(data.keys())
    categories = data['Category_tb']
    products = data['Product_tb']
    merchants = data['Merchant_tb']
    carts = data['Cart_tb']

    # print(categories)
    #print(products)

# My Customer Id, I assume I'm Logged in
Customer_id = 1

# My Cart Query Function
def Get_Cart_Items(id):
    cart_item = carts.values()  # All cart items
    customer_items = {}  # Customer's Cart items

    # Customer's product_id and amount of products
    products_id = [[[],[]]]  # ONly for the Customer
    #products_amount = []
    
    # Iterates through the cart
    for value in cart_item:
        if value['customer_id'] == id: # if cart has the customer's Id
            # add id to products_id list
            products_id[0][0].append(value['product_id'])
            products_id[0][1].append(value['amount'])
            
            #products_amount.append(value['amount'])
    #print(products_id)

    # Include amount of products in cart to customer_items
    for each in products_id:
        pid, amt = each # product_id and amount :)
    
        for prod in products.values():
            # if any if the ids in product in our filtered product id
            if prod['id'] in pid:
                # Quickly add the amount
                prod['amount'] = amt[pid.index(prod['id'])]

                # Let me check for catergory
                for cat in categories.values():
                    if prod['Category_id'] == cat['id']:

                        # if found, do the next thing
                        prod['category_name'] = cat['name']
                        break
                else:
                    # incase nothing happens, We move :)
                    continue
                # Then create an object in customer_items
                customer_items[prod['id']] = prod
        #print(customer_items)
    
    return customer_items

# Create your views here.
def index(request):
    return render(request, 'index.html', {"categories": categories.values(), "products": products.values()})


def product(request):
    return render(request, 'product.html', {})

def checkout(request):
    return render(request, 'checkout.html', {})

def cart(request):
    mode = request.GET.get('mode', None)
    customer_cart = Get_Cart_Items(Customer_id)
    if mode == "dropdown":
        return render(request, 'dropdown_cart.html', {"carts": customer_cart.values()})
    
    return render(request, 'cart.html', {"carts": customer_cart.values()})

def store(request):
    return render(request, 'store.html', {"categories": categories.values(), "products": products.values(), "Merchants":merchants.values()})
