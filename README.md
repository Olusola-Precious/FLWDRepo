# JUMGA MARKETPLACE 
![Bootstrap-3.3.7](https://img.shields.io/badge/Bootstrap-3.3.7-blue "Bootstrap-3.3.7")
![Django==3.1.4](https://img.shields.io/badge/Django-3.1.4-green "Django==3.1.4")
![Flutterwave API V3](https://img.shields.io/badge/FlutterwaveApi-V3-orange "Flask-SQLAlchemy==2.4.4")
![JQuery-3.3.4](https://img.shields.io/badge/JQuery-2.2.4-yellow "JQuery-2.2.4")

> A multi-vendor marketplace ecommerce web applicatiion platform with full online payment solution with the aid of the Flutterwave payment API
> Developed during Flutterwave's Developer Challenge 2021
<hr>
<div align='center'>
  <img src="./static/shop/img/site-banner.jpg" title="Jumga banner" width='100%'>
</div>
<hr>

# Table of Contents
* [Introduction](#Introduction)
* [Setup](#Setup)
* [Testing Data](#Testing)
* [How it works](#How-it-works)
  * [Registration](#Registration)
  * [Store](#Store)
  * [Dispatcher](#Dispatcher)
  * [Shopping and Checkout](#Shopping-and-checkout)
  * [Payment and Calculations](#Payments-and-calculations)
  * [Configuration Parameters](#Configuration-parameters)
* [Upcoming improvements](#Upcoming-improvements)
<hr>

## Introduction
This web application is an ecommerce platform which provides online market features very much similar to that of Jumia, where vendors can register their stores and thier products is published for sale. Notable
features includes:
  * Multicurrency: By default the platform allows customers to switch currency (Dollars(USD), Naira(NGN), Cedi(GH¢)). The default currency is `NGN`, but this could be changed to a desired currency in the environment variable `.env` file by setting the `PRODUCT_PRICING` value [See configurations section](#Configuration-parameters).

  * Vendor Registration Token: Vendors can register, but get thier account approved by paying a token of `$20`. The value of the fee charged for vendor approval can be set/changed value by setting the `STORE_REG_AMT (defaults to 10 USD) value in the config [Read more in the config section]().
  * Dispatcher Assignment: Upon successful registration, a JUMGA dispatcher is randomly assigned to each store.
  * Revenue sharing: For every checked-out order, the total revenue is shared based on the value of the `STORE_PAY_RATIO` and `SPLIT_RATIO_DISPATCHER` configuration values. But by default:
    * Vendor:Jumga = 0.97:0.03 of the product prices
    * Dispatcher:Jumga = 0.80:0.2 of delivery fee.  
  Note: The point at which the splitting occurs is defined by the `PAYMENT_SPLIT_POINT` (defaults to `'instant'`) [see the Configuration section]().

## Setup
1. _[required]_ Install the requirements file by doing ```python -m pip install -r requirements.txt```
2. _[optional]_ During production, it is advisable to set configuration variables as explained in the [configuration section](Configuration Variables) but can be skipped during testing
3. _[optional]_ For testing purpose, if desired some dummy data (products, users, stores, and  dispatchers) can be automatically bootstraped to the database by running ```python create_dummy.py``` [see more](testing)
3. _[required]_ launch the app by doing ```python run.py```

## How it Works
### Registration
<div align='center'>
  <img src="./readme_assets/registration.gif"
    title="Registration process" width='100%'>
</div>

* An anonymous user visits or get redirected to the login page
* Clicks on the sign up link
* Fills the registration form with a unique email address, and instantly got registered and logged-in.




### Store
Any registered user can create a store, after the payment of a store registration fee specified by the `STORE_REG_AMT`(default is 10 USD) configuration variable. After payment has been confirmed, an editable store is automatically generated and a dispatcher got assigned to the new store. An account detail form is also presented to the store owners, the values of which are sent to flutterwave for the creation or modification of subaccounts.  
When multicurrency in set to true, stores are allowed to quote the prices of their products in one of the supported currencies.  
For every store sales, the share of the store owner is picked up from the `SPLIT_RATIO_STORE`(default is 0.975) configuration variable and when the `PAYMENT_SPLIT_POINT` is set to instant, the disbursement is achieved with flutterwaves split payment feature. Check [payments and calculations](#Payments-and-calculations) for more.

### Dispatcher
Dispatchers are created by Jumga, each dispatcher can charge different delivery rates which is specified during creation. Just like the stores, their account details are sent to flutterwave for the creation or modification of subaccounts.
For every product sales, the dispatcher receives `SPLIT_RATIO_DISPATCHER`(default to 0.8) fraction of it's sum of delivery charge. Check [payments and calculations](#Payments-and-calculations) for more.

### Shopping and checking out
* A vistor visit the website, the platform guesses the currency of the visitor from the its IP Address and sets it as a cookie.
based on the visitors currency, values of all products are converted to the visitors' currency value.
* A user selects all the desired products which could possibly be from different stores
* Clicks on checkout when ready and for redirected to the checkout page, where contact information are collected and summary of the impending order is displayed.
* Clicks on paynow will trigger the flutterwave inline payment form with the parsed order details and respective stores and dispatcher split payment arguement when the payment mode is set to instant.

### Payments and Calculations:
Say, a customer ordered for two products, Fanta 30cl and Nokia 2.4


**| Fanta 30cl | Nokia 2.4
---------| ------------- | ------------
Store Name | Cocacola | Nokia
Attached Dispatcher | Kwik | Max
Store Unit price | 10 USD | 59,000 NGN
Quantity | 5 | 2
Cart Unit Price | 470 NGN (1USD = 470NGN) | 59,000 NGN
Total Cart amount | 470* 10 *5 = 23500 NGN | 118,000 NGN
Dispatcher Rate | 1.20 USD | 2 USD
Total cart delivery | 5* 1.2 * 470 = 2820NGN | 2 * 2 * 470 = 1880NGN
Checkout Amount | 23500+2820= 26,320NGN |  118000 + 1880 = 119,880 NGN


In this scenario:
* The customer pays 26320+119880 = 146,200 NGN
* Cocacola gets 23500 * 0.975 = 22,912.50 NGN
* Kwik(Dispatcher attched to Cocacola) gets 2820 * 0.8 = 2,256 NGN
* Nokia gets 118000 * 0.975 = 115,050 NGN
* Max(Dispatcher attched to Cocacola) gets 1880 * 0.8 = 1,504 NGN
* Transaction charges are deducted from Jumga's share


## Configuration Parameters
Variable  | Type / Default | Description
---------- | - | -------
SPLIT_RATIO_STORE | String of float (defaults to  '0.8') | The fraction of the products price to disburse to the store owners, the other fraction goes to the platform
SPLIT_RATIO_DISPATCHER | String of float (defaults to  '0.975') | The fraction of the delivery cost to disburse to the dispatcher, the other fraction goes to the platform
FLW_PUB_KEY | String (defaults to a flutterwave test api value of 'FLWPUBK_TEST-4b5acac8e21aceb3fc87f634a846c001-X'). | Flutterwave's public key for integrating frontend payments, you have to [get yours](https://developer.flutterwave.com/docs/api-keys) to be able to handle payments succesfully.
FLW_SEC_KEY | String (defaults to a flutterwave test api value of 'FLWSECK_TEST-604a7225885949af8eded44c605deb0c-X' | Flutterwave's secret key for backend communications with your flutterwave's account, you have to [get yours](https://developer.flutterwave.com/docs/api-keys) to be able to perform backend activities like confirmation of payments succesfully
PAYMENT_SPLIT_POINT | String (defaults to 'instant') | When to disburse payment to the parties (store and dispatchers) involved. Can be one of `'instant'` (pay each vendors and dispatchers during checkout using subaccount flat split payment), `'fullfil'` (_not_yet_implemented_ pay parties after when an order has been marked as done)
PAYMENT_PLATFORM | String (defaults to 'flutterwave') | The payment platform to use, note that this app is built on modular architecture, thus one can always write modules for other payment system but must really understand what needs to be tweaked, thus the scope of this app is currently for flutterwave payment system which is known for its reliability
PRODUCT_PRICING | String (defaults to 'localize') | The currencu to display the product in. Can be one of: `localize` (converts the products from their store currency to the clients currency based on the conversion rates specified provided the client currency is one stated next, else product prices will be converted to USD); `'GBP'`; `'KES'`; `'NGN'`; `'USD'` (The product prices will be fixed at the specified ISO CODE)
STORE_REG_AMT | String of value+space+code (defaults to '10 USD') | The registration fee to charge Vendors

## Upcoming Improvements
(An evolving list)
* Dispatcher Assignment should be currency-aware
* `pay_after_done` option for the `PAYMENT_SPLIT_POINT` configuration variable: When the `pay_after_done` is used, disbursement of partners payments will only be effected after the order has been marked as delivered by the store owner.