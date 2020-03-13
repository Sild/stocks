#!/usr/bin/python

DEFAULT_PROFIT_COEFF = 0.8
profit_coeff = 0.0
while profit_coeff == 0.0:
    user_input = input("Enter profit coeff (%): ")
    if len(user_input) == 0:
        print("Empty input. Use default coeff: {}%".format(DEFAULT_PROFIT_COEFF))
        profit_coeff = DEFAULT_PROFIT_COEFF
        break
    try:
        profit_coeff = float(user_input.replace(",", "."))
    except Exception as e:
        print("Number expected. Try againg.")
    
inc_multy = 1 + profit_coeff / 100  
dec_multy = 1 - profit_coeff / 100  

while True:
    user_input = input("Enter price: ")
    deal_price = 0
    try:
        deal_price = float(user_input.replace(",", "."))
    except Exception as e:
        print("Float expected. Try again.")
        continue
    print("100% = {}".format(deal_price))
    print("{}% = {}" .format(inc_multy * 100, deal_price * inc_multy))
    print("{}% = {}" .format(dec_multy * 100, deal_price * dec_multy))
