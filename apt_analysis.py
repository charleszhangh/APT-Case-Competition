"""
Created: April 7th, 2017
Program: Applies predictive model to find optimal store time and employee operations for 400+ stores of grocery chain
@author: Charles Zhang
"""

import pandas as pd

# Sources
inputDirectory = 'Input\\'
input_data = inputDirectory + 'aptdata.csv'
outputDirectory = 'Output\\'

# Transforms csv files to data frames
data = pd.read_csv(input_data, encoding="ISO-8859-1",low_memory = False)

#Calculates projected profit
def predictedProfit(avg_pre,associates_poh_post,hours_open_post,competition_within_5,competition_dummy):

    #Multiple Regression Model for Predicted Transactions
    transactions = 80.508038162*associates_poh_post + 373.7047866*hours_open_post + \
                         (-2.017462713 + 1.9499486293*competition_dummy)*competition_within_5 + \
                   1.1077246972*avg_pre - 6998.69983

    #Calculate revenues and costs based on number of transactions
    transaction_profit = transactions*40*.5
    costs = 250*7*hours_open_post + 10*associates_poh_post*hours_open_post*7

    total_profit = transaction_profit-costs
    return(total_profit)

#Cycles through all possible combinations for 483 stores to find optimal combinations
for x,datarow in data.iterrows():
    avg_pre = data.loc[x, 'avg_post']
    associates_poh_post = data.loc[x, 'associates_poh_post']
    hours_open_post = data.loc[x, 'hours_open_post']
    competition_within_5 = data.loc[x, 'competition_within_5']
    competition_dummy = data.loc[x, 'type_dummy']
    possible_associates = [24,26,28]
    possible_hours = [12,13,14]
    optimal_associates = 0
    optimal_hours = 0
    optimal_profit = 0
    for y in possible_associates:
        for z in possible_hours:
            predicted_growth = predictedProfit(avg_pre,y,z,competition_within_5,competition_dummy)
            if (predictedProfit > optimal_profit):
                optimal_profit = predictedProfit
                optimal_associates = y
                optimal_hours = z
    data.loc[x,'optimal_associates'] = optimal_associates
    data.loc[x,'optimal_hours'] = optimal_hours
    data.loc[x,'optimal_growth'] = optimal_profit

data.to_csv(outputDirectory + 'optimized_combinations.csv')

