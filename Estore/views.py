from django.shortcuts import render, redirect
from pathlib import Path
import os
import json
from django.http import HttpResponse

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

# My Customer Id, I assumed I'm Logged in
Customer_id = 1

# My Cart Query Function
def Get_Cart_Items(id):
    cart_item = carts.values()  # All cart items
    customer_items = {}  # Customer's Cart items

    # Customer's product_id and amount of products
    products_id = [[[],[]]]  # ONly for the Customer
    product_prices = []
    
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
                product_prices.append(prod['Price'])

                # Let me check for catergory
                for cat in categories.values():
                    if prod['Category_id'] == cat['id']:

                        # if found, do the next thing
                        prod['category_name'] = cat['name']
                        break
                

                # Then create an object in customer_items
                customer_items[prod['id']] = prod
        #print(customer_items)
    # print(sum(product_prices))
    
    return customer_items, sum(product_prices)

# Write to Json File
# function to add to JSON
def write_json(data, filename=data_Path):
    with open(filename, 'w') as f:

        json.dump(data, f, indent=4)

# Save New Json to update Previous Json
def SaveJSON(new_dict, filename=data_Path):
    
    with open(filename) as json_file:
        data = json.load(json_file)

        data['Cart_tb'] = new_dict
        #print(data)
    write_json(data)


def Add_to_cart(customer_id, prod_id, qty):
    global carts
    last_cart = list(map(int, carts.keys()))[-1] # recently added cart id
    
    new_cart = {}

    for c in carts.values():
        
        if c['product_id'] == prod_id:
            
            c['amount'] = qty
            new_cart = c
            
            break
    else:
        new_cart['id'] = last_cart + 1
        new_cart['customer_id'] = customer_id
        new_cart['product_id'] = prod_id
        new_cart['amount'] = qty
        new_cart['date_added'] = ""

        carts[last_cart + 1] = new_cart

    SaveJSON(carts)
    #print(new_cart)
    #print(carts)


def Rem_from_cart(customer_id, prod_id):
    global carts

    new_cart = {}

    cart_id = None

    for c in carts.values():
        if (c['product_id'] == prod_id) and (c['customer_id'] == customer_id):
            cart_id = c['id']
    
    carts.pop(str(cart_id))
    SaveJSON(carts)
    
def Clear_cart(customer_id):
    global carts
    
    prod_id = []

    for cid in carts.values():
        if cid['customer_id'] == customer_id:
            prod_id.append(cid['id'])
    # print(prod_id)

    for id in prod_id: carts.pop(str(id))
    SaveJSON(carts)

    



# Create your views here.
def index(request):
    # id = request.session.get('merchant_id', None)

    return render(request,'index.html', {"categories": categories.values(), "products": products.values()})


def product(request):
    product_id = request.GET.get('product', None)
    
    product_to_view = {}
    product_category = {}
    product_in_category = {}
    if product_id is not None:
        for prod in products.values():
            if prod['id'] == int(product_id):
                product_to_view = prod
                product_category = categories[str(prod['Category_id'])]
                break
        for cat_prod in products.values():
            if cat_prod['Category_id'] == product_category['id']:
                product_in_category[cat_prod['id']] = cat_prod

        # print(product_in_category)
        return render(request, 'product.html', {"product": product_to_view, "category": product_in_category.values()})
    return render(request, 'product.html', {})

def checkout(request):
    customer_cart, Total = Get_Cart_Items(Customer_id)
    # Clear_cart(Customer_id)
    return render(request, 'checkout.html', {"carts": customer_cart.values(), "total_price": Total})

def cart(request):
    mode = request.GET.get('mode', None)
    customer_cart, Total = Get_Cart_Items(Customer_id)
    if mode == "dropdown":
        return render(request, 'dropdown_cart.html', {"carts": customer_cart.values(), "total_price": Total})
    elif mode == "qty":
        lent = str(len(customer_cart))
        return HttpResponse(lent)
    elif mode == "add":
        prod_id = request.GET.get('prod', None)
        quantity = request.GET.get('qty', None)
        # print(prod_id, quantity)
        Add_to_cart(Customer_id,int(prod_id), int(quantity))
        return redirect('cart')
    elif mode == "del":
        prod_id = request.GET.get('prod', None)
        Rem_from_cart(Customer_id, int(prod_id))
        # return redirect('cart')


    
    return render(request, 'cart.html', {"carts": customer_cart.values(), "total_price": Total})

def store(request):
    customer_cart = Get_Cart_Items(Customer_id)[0]
    
    return render(request, 'store.html', {"categories": categories.values(), "products": products.values(), "Merchants": merchants.values(), "carts": customer_cart.values()})

