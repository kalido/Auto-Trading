from calendar import prcal
from doctest import Example
import os.path
from time import sleep 
import bitso
import keyboard

def getKeys():
    if os.path.exists("keys.txt"): 
        keys = open('keys.txt', 'r')
        keys = keys.readlines()
        api_key = str(keys[0].strip())
        api_secret = str(keys[1].strip())
    else:
        print('file not found please add it')
    api = bitso.Api(api_key, api_secret)

    return api

def conection_test(api):
    conectionTest = api.account_status()
    print("\n ID User Confirmed:", conectionTest)

def fullScreen():
    keyboard.press('Command + Return')

def monitor(api,mkt,times):
    now = api.ticker(mkt).bid
    print('First monitored price:', now,"\n")
    for i in range(times):
        prices = api.ticker(mkt).bid
        if prices > now:
            print(prices,"➚")
            now = prices
        elif prices == now:
            print('----⮕')
        else:
            print(prices,"➘")
            now = prices
        sleep(3) #Prevent server block
    
def btcBalance(api,mkt):
    balance = api.balances() 
    balance_details = balance.__dict__
    btc = balance_details[mkt.split('_')[0]].available
    return btc

def mxnBalance(api,mkt):
    balance = api.balances() 
    balance_details = balance.__dict__ 
    pesos = balance_details[mkt.split('_')[1]].available

    return pesos

def hightestBuyPrice(api,mkt):
    posture = api.ticker(mkt)
    print("\nHighest buy price:", posture.bid,"Data:", posture.created_at)

def buy_cripto(api,mkt):
    posture = api.ticker(mkt)
    while True:
        amount = float(input("Set a value like " + str(posture.bid) + " or less\n" + "===> "))

        if amount < float(posture.bid):
            break
        else:
            print('BE CAREFUL! try again.')
    sample = mxnBalance(api,mkt)
    butget = format(float(input('Amount: (Example: ' + str(sample) + 'or less):' ))/amount, '.8f')
    new_order = api.place_order(book = mkt, side = 'buy', order_type = 'limit', major=str(butget), price=str(amount))
    print('New Order Created:', new_order['oid'])

def sell_cripto():
    print('sell cripto')

def deleteAnOrder(api,mkt):
    openOrders = api.open_orders(mkt)
    if openOrders == []:
        print('No open order found')
    else:
        print("You've:", len(openOrders), "order(s)\n")
        for order_o in openOrders:
            print("| Order ID:", order_o.oid, "| Position:", order_o.side, "| Amount:", order_o.price, "| Original amounts:", order_o.original_amount)
            print("------------------------------------------------------------------------------------------------")
        close_order = api.cancel_order(str(input("Type an oID to delete: ")))
        if not close_order == []:
            print('Order successfully canceled!')
        else:
            print('Order not found!')

def deleteAllOrders(api,mkt):
    opened_orders = api.open_orders(mkt)
    if opened_orders == []:
        print('No open order found')
    else:
        print("Order(s) found:",len(opened_orders),"\n")
        for order in opened_orders:
            print('Order ID:', api.cancel_order(order.oid), '-> Order Removed')
