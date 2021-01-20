# JUMGA MARKETPLACE 
![Bootstrap-3.3.7](https://img.shields.io/badge/Bootstrap-3.3.7-blue "Bootstrap-3.3.7")
![Django==3.1.4](https://img.shields.io/badge/Django-3.1.4-green "Django==3.1.4")
![Flutterwave API V3](https://img.shields.io/badge/FlutterwaveApi-V3-orange "Flask-SQLAlchemy==2.4.4")
![JQuery-3.3.4](https://img.shields.io/badge/JQuery-2.2.4-yellow "JQuery-2.2.4")

> A multi-vendor marketplace ecommerce web applicatiion platform with full online payment solution with the aid of the Flutterwave payment API
> Developed during Flutterwave's Developer Challenge 2021.
<hr>



# Table of Contents
* [Introduction](#Introduction)
* [Setup](#Setup)
* [Testing Data](#Testing)
* [How it works](#How-it-works)
  * [Registration](#Registration)
  * [Store](#Store)
  * [Dispatcher](#Dispatcher)
  * [Shopping and checking out](#Shopping-and-checkout)
  * [Payment and Calculations](#Payments-and-calculations)
  * [Configuration Parameters](#Configuration-parameters)
* [Upcoming improvements](#Upcoming-improvements)
<hr>

## Introduction
This web application is an ecommerce platform which provides online market features very much similar to that of Jumia, where vendors can register their stores and thier products is published for sale. Notable
features includes:
  * Multicurrency: By default the platform allows customers to switch currency (Dollars(USD), Naira(NGN), Cedi(GH¢)). The default currency is `NGN`, but this could be changed to a desired currency in the environment variable `.env` file by setting the `PRODUCT_PRICING` value [See configurations section](#Configuration-parameters).

  * Vendor Registration Token: Vendors can register, but get their account approved by paying a token of `$20`. The value of the fee charged for vendor approval is set as a context in `payment.views.pay` view (defaults to 20 USD).

  * Dispatcher Assignment: Upon successful registration, a dispatcher is randomly assigned to each vendor.

  * Revenue sharing: For every completed order, the total revenue is shared based on the value of the `DELIVERY_FEE` and dispatcher percentage as calculated below:
    * Vendor:Jumga = 0.97:0.03 of the product prices
    * Dispatcher:Jumga = 0.80:0.2 of delivery fee from value of `DELIVERY_FEE` in `.env` file.  
  
  Note: You are to create a `.env` file in the in the same directory with this ReadMe file.

## Setup
<hr>
1. _[required]_ Install the requirements file by doing ```python -m pip install -r requirements.txt```
2. _[optional]_ During production, it is advisable to set Django module setting in your enviroment variable `.env` file to production as explained in the [configuration section](Configuration Variables) but can be skipped during testing as the default will be in development.

3. _[required]_ start the app by running ```python manage.py runserver``` at the console.

# How it Works
## Registration


####  Customer

* A Customer visits, order/add to cart or get redirected to the login page
* if customer dont have an account, Clicks on the create account link
* Fills the registration form with a unique email address which will be used to login other times, and instantly got registered and logged-in.

####  Vendor

* A Vendor visits and directed to the Vendor login page
* if vendor doesn't have an account, Clicks on the Become a seller link
* Fills the registration form including a unique email address which will be used to login other times, and instantly got registered and logged-in,
other information collected will include account Number, Account Name, e.t.c, of which will be needed when dealing with creation of sub accounts and splitting of payments.
but account won't be approved until payment is made.



## Store

<hr>
Any Approved Vendor can create a store if the Vendor has been approved, after the payment of a Vendor registration fee specified by the `fee` variable (default is 20 USD) in `payment.views.pay`. After payment has been made, the `transaction_id` is sent to the `payment.views.verify` view to confirm the transaction using the `https://api.flutterwave.com/v3/transactions/{transaction_id}/verify` endpoint, and the status is used to determine if the vendor should be approved or not. If status is `successful` then the vendor is approved, else not. if the vendor is confirmed to have paid the required token, such vendor will be assigned a dispatcher,and can create as many stores as possible on the vendor account.  
When multicurrency in set to true, vendors are allowed to quote the prices of their products in one of the supported currencies.
For every store sales of the vendor, the share of the vendor(which is the store owner) is calculated which is by default 97.5% (i.e 0.975 of the total sale of product of vendor), the disbursement is achieved with flutterwaves split payment feature. Check [payments and calculations](#Payments-and-calculations) for more.

### Dispatcher
Dispatchers are created by Jumga, each dispatcher's rate is 80% of `DELIVERY_FEE` value. Just like the stores, their account details are sent to flutterwave for the creation or modification of subaccounts.
For every product sales, the dispatcher receives `80%` (i.e 0.8) fraction of `DELIVERY_FEE` value. Check [payments and calculations](#Payments-and-calculations) for more.

## Shopping and checking out
<hr>
* A vistor visit the website, the platform auto-detects the currency of the visitor from the its IP Address and sets it as a cookie.
based on the visitors currency, values of all products are converted to the visitors' currency value, but all currencies are stored in dollars in the databse.

* A user selects all the desired products which could possibly be from different stores
* Clicks on checkout when ready and redirected to the checkout page, where contact information are collected and summary of the impending order is displayed.
* Clicks on place Order button and it'll trigger the flutterwave inline payment form with the parsed order details and respective stores and dispatcher split payment arguement.

### Payments and Calculations:
<hr>
Assuming a customer orders for two products, Head phone and Samsum Phone.


 ** Payments|   and   | Calculations 
---------| ------------- | ------------
Products | Wireless Head Phone | Galaxy S8
Vendor Names | Wires.inc | Samsung
Attached Dispatcher for order | Kvewe
Store Unit price | 75 USD | 250 USD
Quantity | 3 | 1
Cart Unit Price | 350 NGN |(1USD = 350NGN) 
NGN_conversion | 26,250 NGN | 87,500 NGN
Total Cart amount | 75 * 3 + 250 * 1 (26,250 * 3 + 87,500 * 1) | = 475 USD (166,250 NGN)
Dispatcher Rate | 120 USD (80%) | `of DELIVERY_FEE` value (default is 150 USD)
Total cart + delivery | 475 USD + 150 USD |= 625 USD (218,750 NGN) 
Checkout Amount | 625 USD | (218,750 NGN)


In this scenario:
* The customer pays 625 USD = 218,750.00 NGN
* Wires.inc gets 225 USD = 78,750.00 NGN
* Kwik(Dispatcher attched to Cocacola) gets 60 USD = 21,000 NGN
* Nokia gets 250 USD = 87,500 NGN
* Max(Dispatcher attched to Cocacola) gets 60 USD = 21,000 NGN
* Transaction charges are deducted from Jumga's commision.
<hr>

## Configuration Parameters

The following are the configuration of `Environment variables`.

Note: You'll have to create an `.env` file in the same directory with this readme file.


Variable  | Type / Default | Description
---------- | - | -------
DJANGO_SETTINGS_MODULE | String of project's mode (either `Eecommerce.settings.development` or `Eecommerce.settings.production`. defaults to  `Eecommerce.settings.development`) | The settings of this app is splitted into development and production, on seperate concerns, (Debug, Database, e.t.c).files are located at `Eecommerce.settings` directory.
ACCESS_TOKEN | String (Flutterwave `SECRET_KEY` provided on the dashboard) | This is the flutterwave API `SECRET_KEY` provided on the flutterwave dashboard.
SECRET_ADMIN_URL | String (defaults to `venom_admin`). | django admin Url. run `python manage.py createsuperuser` to create superuser for django project administration.
APP_NAME | String (defaults to JUMGA) | Projects WebApp Name
NORMAL_CURRENCY | String (defaults to `NGN`) | Currency used in the `currency` parameter in the Flutterwave inline Js script.
PAYMENT_PLATFORM | String (defaults to 'flutterwave') | The payment platform to use, note that this app is built on modular architecture, thus one can always write modules for other payment system but must really understand what needs to be tweaked, thus the scope of this app is currently for flutterwave payment system which is known for its reliability
PRODUCT_PRICING | String (defaults to `NGN`) | The currency to display the product.
DELIVERY_FEE | Float of price value (defaults to `150`  in USD) | The registration fee to charge Vendors for approval of account.
SECRET_KEY | String offered by  django project | App Secret key hidden :).
PUBLIC_KEY | String | Public_KEY API key from flutterwave Dashboard.

<hr>

## Upcoming Improvements
(An evolving list)
* Any further progress on this project, will be implemented and will reflect in this ReadMe file :).