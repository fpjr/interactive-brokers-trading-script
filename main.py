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
import logging
import time
import datetime


# paper trading port
port = 7497 # 7496 for live tradig, 7497 for paper trading 
marketDataType = 3 # 3 for delayed, 1 for realtime. https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#ae03b31bb2702ba519ed63c46455872b6

# set type of data to request from API
requestType = "tick-by-tick"

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
        
        # define request market data type
        #self.reqMarketDataType(marketDataType)
        
        # snapshot = False refers to stream of market data, requires active market data subscription
        # regulatorySnapshot = False, no relevant regulatory snapshot; one time fee 1 cent USD per snapshot
        #self.reqMktData(orderId, mycontract, "", False, False, [])
        
        
     # this is used for price values from market data request   
    #def tickPrice(self, reqId, tickType, price, attrib): 
        # print returned value from ticket price
     #   print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}")
        
    # indicate bit size, ask size, daily volume
    #def tickSize(self, reqId, tickType, size):
     #   print(f"tickSize. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, size: {size}")
    
    def realtimeBar(self, reqId: TickerId, time:int, open_: float, high: float, low: float, close: float, volume: Decimal, wap: Decimal, count: int):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count))
   
    
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
    pass


class ExecuteTrade():
    pass


def main():
    SetupLogger()
    logging.debug("now is %s", datetime.datetime.now())
    logging.getLogger().setLevel(logging.ERROR)
    
    testapi = DataFetching()
    testapi.connect('127.0.0.1', port, clientId=0)
    testapi.run()
    
    # testplaceorder = TestPlaceOrder()
    # testplaceorder.connect('127.0.0.1', port, clientId=0)
    # testplaceorder.run()

if __name__ == "__main__":
    main()