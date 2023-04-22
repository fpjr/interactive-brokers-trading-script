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

def main():
    pass
    # testapi = TestAPI()
    # testapi.connect('127.0.0.1', port, clientId=0)
    # testapi.run()
    
    # testplaceorder = TestPlaceOrder()
    # testplaceorder.connect('127.0.0.1', port, clientId=0)
    # testplaceorder.run()

if __name__ == "__main__":
    main()