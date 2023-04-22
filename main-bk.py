#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 08:52:29 2023

@author: fred
"""
#https://interactivebrokers.github.io/tws-api/basic_orders.html

from ibapi.client import *
from ibapi.wrapper import *


# paper trading port
port = 7497

class TestAPI(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId: int):
        #self.reqScannerParameters() # to request an xml market scanner queries
        
        mycontract = Contract()
        mycontract.symbol = "IBKR" # ticker
        mycontract.secType = "STK" # security's type
        mycontract.exchange = "SMART" # destination exchange
        mycontract.currency = "USD"
        
        # define market data type
        self.reqMarketDataType(3) # 3 for delayed, 1 for realtime. https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#ae03b31bb2702ba519ed63c46455872b6
        
        # snapshot = 0; refers to stream of market data, requires active market data subscription
        # regulatorySnapshot = 0; no relevant regulatory snapshot; one time fee 1 cent USD per snapshot
        self.reqMktData(orderId, mycontract, "", 0, 0, [])
        
        
     # this is used for price values from market data request   
    def tickPrice(self, reqId, tickType, price, attrib): 
        # print returned value from ticket price
        print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}")
        
    # indicate bit size, ask size, daily volume
    def tickSize(self, reqId, tickType, size):
        print(f"tickSize. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, size: {size}")
    
    
    def scannerParameters(self, xml): # save requested scanner parameters
        dir = "/Users/fred/scripts/tws/scanner.xml"
        open(dir, 'w').write(xml) # write requested xml
        print("Scanner parameters saved")
        

class TestPlaceOrder(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId: int):
        mycontract = Contract()
        mycontract.symbol = "IBKR"
        mycontract.secType = "STK" # security's type
        mycontract.exchange = "SMART" # destination exchange
        mycontract.currency = "USD"
        
        self.reqContractDetails(orderId, mycontract)
    
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract)
        
        myorder = Order()
        myorder.orderId = reqId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        myorder.totalQuantity = 10
        
        self.placeOrder(reqId, contractDetails.contract, myorder)
        self.disconnect()
                     
                     
class TestComplexOrder(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId: int):
        mycontract = Contract()
        mycontract.symbol = "IBKR"
        mycontract.secType = "STK" # security's type
        mycontract.exchange = "SMART" # destination exchange
        mycontract.currency = "USD"
        
        self.reqContractDetails(orderId, mycontract)
    
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract)
        
        myorder = Order()
        myorder.orderId = reqId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        myorder.totalQuantity = 10
        
        self.placeOrder(reqId, contractDetails.contract, myorder)
        self.disconnect()
        

def main():
    # testapi = TestAPI()
    # testapi.connect('127.0.0.1', port, clientId=0)
    # testapi.run()
    
    # testplaceorder = TestPlaceOrder()
    # testplaceorder.connect('127.0.0.1', port, clientId=0)
    # testplaceorder.run()

if __name__ == "__main__":
    main()