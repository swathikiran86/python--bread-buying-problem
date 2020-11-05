"""
Name: Swathikiran Srungavarapu
email: swathikiran86@gmail.com

Description:
1. The solution provided below calculates the best possible outcomes with least cost for a given input with any number of sellers.
2. I have taken into consideration all factors to optimise the cost and handled the input accordingly to always give the cheapest cost as output. 
    This is implemented in the function "getPlanListByPrice"
3. I have also considered and implemented the tie breaking situation. For this, I have computed 
    (a) Least cost for a given input via the function "getPlanListByPrice"
    (b) Least number of sellers for a given input via the function "getPlanListBySellers"
    Then, I have compared the output from functions (a) and (b) to calculate the least cost.
    In case, the cost given by function (a) is lesser than (b) then the output from (a) would be the final output.
    Else, in case the cost given by function (a) is greater than or eaual to (b) then the output from (b) would be the final output.
    This way, in case of a tie, my program handles to provide least cost with least number of sellers.
4. Test Cases:
    a) Input with complex prices 
        input = [60, (10,100),(20,100),(30,300),(45,50),(55,40),(59,50)]
        output = [10, 25, 'None', 10, 5, 'None']
    b) Input with equal cost for from all the sellers - (tie breaker situation)
        input = [60,(10,100), (15,100), (35,100), (50,100)]
        output = [30, 'None', 20, 'None']
    c) Input with less than 30 days
        input= [29,(10,100), (15,100), (25,100), (28,50)]
        output = [18, 'None', 'None', 1]
    d) Input with first seller arriving before the 10th day
        input = [60,(8,100), (15,100), (35,100), (50,100)]
        output = [28, 'None', 22, 'None']
    e) Input with first seller arriving after the 10th day
        input = [60,(12,100), (15,100), (35,100), (50,100)]
        output = Invalid Input


Assumptions:

1. If the first seller is arrived later than 10th day, I have asssumed that the family will be deprived of bread.
    I have handled this condition and an "Invalid input" message is printed.

2. I have considered that the sellers will be frequent enough so that the customer isn't deprived of bread.
    That is, the gap between two sellers arrival will always be less than or equal to 30.
    This can be handled in the code. However, due to time constraints I havent implemented this.

"""


#importing the libraries
import pandas as pd
import numpy as np
import sys
import re
import numbers



# function to calculate the best possible output with minimum cost
def calculate_purchasing_plan(total_no_days, sellers):

    #function to calculate the best optimal price 
    planListByPrice = getPlanListByPrice(total_no_days,sellers)

    #Calculating the cost total from the list output by getPlanListByPrice
    planListByPrice_total_cost = 0
    for i in range(0,len(planListByPrice)):
        if isinstance(planListByPrice[i], numbers.Number):
            planListByPrice_total_cost = planListByPrice_total_cost + (planListByPrice[i]*sellers[i][1])
        else:
            continue

    #function to calculate the less number of sellers when possible 
    planListBySellers = getPlanListBySellers(total_no_days,sellers)

    #Calculating the cost total from the list output by getPlanListBySellers
    planListBySellers_total_cost = 0
    for i in range(0,len(planListBySellers)):
        if isinstance(planListBySellers[i], numbers.Number):
            planListBySellers_total_cost = planListBySellers_total_cost + (planListBySellers[i]*sellers[i][1])
        else:
            continue

    #print(planListByPrice_total_cost)
    #print(planListBySellers_total_cost)
    #print(planListByPrice)
    #print(planListBySellers)
     
    
    if planListByPrice_total_cost < planListBySellers_total_cost:
        #print(planListByPrice)
        return planListByPrice
    else:
        #print(planListBySellers)
        return planListBySellers

#function to claculate the cheapest price avaiable in next 30 days from other sellers       
def current_cheap_price(seller_id, input_list):
    cheap_price = sys.maxsize
    cheap_price_index = 0
    cheap = []
    
    for x in range(seller_id+1, len(input_list)):
        current_day = input_list[x][0]
        current_price = input_list[x][1]
        start_day = input_list[seller_id][0]
        if current_day - start_day <30:
            if current_price < cheap_price:
                cheap_price = current_price
                cheap_price_index = x
        else:
            break
    cheap.append(input_list[cheap_price_index][0])
    cheap.append(cheap_price)
    
    return cheap

#function to calculate if there is sufficiency of breads 
def isEnough(remaining_breads, current_index, input_list, total_days):
    isSufficient = True
    current_day =input_list[current_index][0]
    if current_index  == len(input_list)-1:
        upcoming_seller_day = total_days
    else:
        upcoming_seller_day = input_list[current_index+1][0]
    
    if remaining_breads < (upcoming_seller_day - current_day):
        isSufficient = False

    return isSufficient


#function to get the best optimal price from the given input list
def getPlanListByPrice(total_no_days,input_list):

    total_days = total_no_days
    max_buy =30
    #current_stock = 10
    current_price =0
    current_day =0
    next_cheapest_day_within_30days = 0
    next_chepeast_price_within_30day = 0
    breads_to_buy = 0
    remaining_breads = 10 - input_list[0][0]
    #print(remaining_breads)
    check_remaining_breads = True
    isLastSeller = False
    bought = False
    planList = []

    for seller in input_list:
        final =[]
        if input_list.index(seller) < len(input_list) -1:
            final = current_cheap_price(input_list.index(seller), input_list)
            next_day = input_list[input_list.index(seller)+1][0]
            next_day_price = input_list[input_list.index(seller)+1][1]

        else:
            isLastSeller = True
            final.append(input_list[input_list.index(seller)][0])
            final.append(input_list[input_list.index(seller)][1])

        current_day = input_list[input_list.index(seller)][0]
        current_price = input_list[input_list.index(seller)][1]
        next_cheapest_day_within_30days = final[0]
        next_chepeast_price_within_30day = final[1]

        if not isLastSeller:
            if current_price >= next_chepeast_price_within_30day:
                isSufficient = isEnough(remaining_breads,input_list.index(seller), input_list,total_days)
                if not isSufficient:
                    breads_to_buy = (next_cheapest_day_within_30days - current_day) - remaining_breads
                    remaining_breads = (remaining_breads +breads_to_buy)- (next_day - current_day)
                    planList.append(breads_to_buy)
                    check_remaining_breads = True
                    bought = True
                else:
                    bought = False
                    remaining_breads = remaining_breads - (next_day - current_day)

            else:
                isSufficient = isEnough(remaining_breads,input_list.index(seller), input_list,total_days)
                if not isSufficient:
                    if (total_days - current_day) >= max_buy:
                        breads_to_buy = max_buy - remaining_breads
                        remaining_breads = (remaining_breads + breads_to_buy)- (next_day - current_day)
                    else:
                        breads_to_buy = (total_days - current_day) - remaining_breads
                        remaining_breads = max_buy - (next_cheapest_day_within_30days - current_day)

                    planList.append(breads_to_buy)
                    check_remaining_breads = True
                    bought = True

                else:
                    bought = False
                    remaining_breads = remaining_breads - (next_day-current_day)

        else:
            isSufficient = isEnough(remaining_breads,input_list.index(seller), input_list,total_days)
            if not isSufficient:
                breads_to_buy = (total_days - current_day) - remaining_breads
                planList.append(breads_to_buy)
                bought = True
            else:
                bought = False
                remaining_breads = remaining_breads - (total_days - current_day)

        if not bought:
            planList.append("None")

    return planList  


#function to return the best optimal solution with less number of sellers
def getPlanListBySellers(total_no_days,input_list):
    total_days = total_no_days
    max_buy =30
    #current_stock = 10
    current_price =0
    current_day =0
    next_cheapest_day_within_30days = 0
    next_chepeast_price_within_30day = 0
    breads_to_buy = 0
    #remaining_breads = 0
    remaining_breads = 10 - input_list[0][0]
    #print(remaining_breads)
    check_remaining_breads = True
    isLastSeller = False
    bought = False
    planList = []
    for seller in input_list:
        final =[]
        if input_list.index(seller) < len(input_list) -1:
            final = current_cheap_price(input_list.index(seller), input_list)
            next_day = input_list[input_list.index(seller)+1][0]
            next_day_price = input_list[input_list.index(seller)+1][1]
        else:
            isLastSeller = True
            final.append(input_list[input_list.index(seller)][0])
            final.append(input_list[input_list.index(seller)][1])

        current_day = input_list[input_list.index(seller)][0]
        current_price = input_list[input_list.index(seller)][1]
        next_cheapest_day_within_30days = final[0]
        next_chepeast_price_within_30day = final[1]

        if not isLastSeller:
            if current_price > next_chepeast_price_within_30day:
                isSufficient = isEnough(remaining_breads,input_list.index(seller), input_list,total_days)
                if not isSufficient:
                    breads_to_buy = (next_cheapest_day_within_30days - current_day) - remaining_breads
                    remaining_breads = (remaining_breads +breads_to_buy)- (next_day - current_day)
                    planList.append(breads_to_buy)
                    check_remaining_breads = True
                    bought = True
                else:
                    bought = False
                    remaining_breads = remaining_breads - (next_day - current_day)

            else:
                isSufficient = isEnough(remaining_breads,input_list.index(seller), input_list,total_days)
                if not isSufficient:
                    if (total_days - current_day) >= max_buy:
                        breads_to_buy = max_buy - remaining_breads
                        remaining_breads = (remaining_breads + breads_to_buy)- (next_day - current_day)
                    else:
                        breads_to_buy = (total_days - current_day) - remaining_breads
                        remaining_breads = max_buy - (next_cheapest_day_within_30days - current_day)

                    planList.append(breads_to_buy)
                    check_remaining_breads = True
                    bought = True

                else:
                    bought = False
                    remaining_breads = remaining_breads - (next_day-current_day)

        else:
            isSufficient = isEnough(remaining_breads,input_list.index(seller), input_list,total_days)
            if not isSufficient:
                breads_to_buy = (total_days - current_day) - remaining_breads
                planList.append(breads_to_buy)
                bought = True
            else:
                bought = False
                remaining_breads = remaining_breads - (total_days - current_day)

        if not bought:
            planList.append("None")

    return planList 

def main():
    #input as it is from the question

    input_values = [60, (10,200),(15,100),(35,500),(50,30)]
    #input_values = [60, (10,100),(20,100),(30,300),(45,50),(55,40),(59,50)]
    #input_values = [60,(10,100), (15,100), (35,100), (50,100)]
    #input_values = [29,(10,100), (15,100), (25,100), (28,50)]
    #input_values = [60,(8,100), (15,100), (35,100), (50,100)]
    #input_values = [60,(12,100), (15,100), (35,100), (50,100)]


    #extracting number of days from input
    total_no_days = input_values[0]
    
    #extracting number of sellers and the price list from the input 
    input_list = input_values[1:]

    #Condition to check if the family will survive till the first seller arrival
    if input_list[0][0] > 10:
        print("Invalid Input")
        
    else:
        #calling the function to provide the output
        result = calculate_purchasing_plan(total_no_days,input_list)
        print(result)

if __name__== "__main__":
  main()
