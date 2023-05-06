#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 08:52:29 2023

@author: fred
"""
#https://interactivebrokers.github.io/tws-api/basic_orders.html

import os

from ibapi.client import *
from ibapi.wrapper import *

import numpy as np
import pandas as pd
import logging
import time
import datetime


# paper trading port
port = 7497 # 7496 for live tradig, 7497 for paper trading 
marketDataType = 3 # 3 for delayed, 1 for realtime. https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#ae03b31bb2702ba519ed63c46455872b6

# set type of data to request from API
requestType = "5sec"

ma5 = np.array([])
ma20 = np.array([])

def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.DEBUG,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logger.addHandler(console)
    
class DataFetching(EClient, EWrapper):    
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId: int):
        #self.reqScannerParameters() # to request an xml market scanner queries
        
        contract = Contract();
        contract.symbol = "ETH";
        contract.secType = "CRYPTO";
        contract.currency = "USD";
        contract.exchange = "PAXOS";
        
        # contract = Contract()
        # contract.symbol = "EUR"
        # contract.secType = "CASH"
        # contract.currency = "GBP"
        # contract.exchange = "IDEALPRO"
        
        # define request market data type
        self.reqMarketDataType(marketDataType)
        
        if requestType == "tick-by-tick":
            # tickType = Last
            # numberOfTicks = 0
            # ignoreSize = True
            self.reqTickByTickData(orderId, contract, "Last", 0, True)   
        
        elif requestType == "historical":
            # use regular trading hours = 1
            self.reqHistoricalTicks(orderId, mycontract,
                               "20170712 21:39:33 US/Eastern", "", 10, "TRADES", 1, True, [])
        
        elif requestType == "5sec":
            self.reqRealTimeBars(orderId, contract,5, "MIDPOINT", True, [])
            
            
        else:
            pass
    
    def realtimeBar(self, reqId: TickerId, time:int, open_: float, high: float, low: float, close: float, volume: Decimal, wap: Decimal, count: int):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count))
        
        GenerateBasicTradingSignals.compute(close)
    
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float, size: Decimal, tickAtrribLast: TickAttribLast, exchange: str, specialConditions: str):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAtrribLast, exchange, specialConditions)
        if tickType == 1:
            print("Last.", end='')
        else:
            print("AllLast.", end='')
        print(" ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
              "Price:", floatMaxString(price), "Size:", decimalMaxString(size), "Exch:" , exchange,
              "Spec Cond:", specialConditions, "PastLimit:", tickAtrribLast.pastLimit, "Unreported:", tickAtrribLast.unreported)
    
    # scan market parameters
    def scannerParameters(self, xml): # save requested scanner parameters
        dir = os.getcwd() + "/scanner.xml"
        open(dir, 'w').write(xml) # write requested xml
        print("Scanner parameters saved")


class GenerateBasicTradingSignals():
    
    def compute(close):
        global ma5
        global ma20
        
        ma5 = np.append(ma5, close)
        ma20 = np.append(ma20, close)
        
        ma5series = pd.Series(ma5)
        ma20series = pd.Series(ma20)
        
        
        print("5-day moving average: ", ma5series.rolling(5).mean())
        print("20-day moving average: ", ma20series.rolling(20).mean())
        
        if not np.isnan(ma5series.rolling(5).mean().iloc[-1]) and not np.isnan(ma5series.rolling(20).mean().iloc[-1]):
            print("not null")
            ExecuteTrade().submitOrder("BUY", 10)
            
            
    def generateTradingSignal():
        pass
        
class ExecuteTrade(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    
    def nextValidId(self, orderId: int):
        mycontract = Contract()
        mycontract.symbol = "IBKR"
        mycontract.secType = "STK" # security's type
        mycontract.exchange = "SMART" # destination exchange
        mycontract.currency = "USD"
        
        self.submitOrder(orderId, mycontract, "BUY", 20)
        
    def submitOrder(self, reqId: int,  contractDetails: ContractDetails, action, quantity):
        order = Order()
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = quantity

        self.placeOrder(reqId, contractDetails, order)
        self.disconnect()

def main():
    SetupLogger()
    logging.debug("now is %s", datetime.datetime.now())
    logging.getLogger().setLevel(logging.DEBUG)
    
    # testapi = DataFetching()
    # testapi.connect('127.0.0.1', port, clientId=0)
    # testapi.run()
    
    executeTrade = ExecuteTrade()
    executeTrade.connect('127.0.0.1', port, clientId=0)
    executeTrade.run()

if __name__ == "__main__":
    main()