"""
Created: April 7th, 2017
Program: Creates multiple regression model to optimize store time and employee operations
@author: Charles Zhang
"""

import pandas as pd
from scipy import stats
import statsmodels.api as sm
import numpy as np

# Sources
inputDirectory = 'Input\\'
input_financials = inputDirectory + 'financials.csv'
input_storemaster = inputDirectory + 'storemaster.csv'
outputDirectory = 'Output\\'

# Transforms csv files to data frames
financials = pd.read_csv(input_financials, encoding="ISO-8859-1",low_memory = False)
storemaster = pd.read_csv(input_storemaster, encoding="ISO-8859-1",low_memory = False)

# Organizes operations data (store opening times and number of associates per hour)
for x,financialsrow in financials.iterrows():
    pre_total_transactions_count = financials.loc[x,'12_14_2014'] + financials.loc[x,'12_21_2014'] +\
                                   financials.loc[x,'12_28_2014'] + \
    financials.loc[x, '1_4_2015'] +financials.loc[x,'1_11_2015'] +financials.loc[x,'1_18_2015'] +\
                                   financials.loc[x,'1_25_2015'] + \
    financials.loc[x, '2_1_2015'] +financials.loc[x,'2_8_2015'] +financials.loc[x,'2_15_2015'] + \
    financials.loc[x, '2_22_2015'] +financials.loc[x,'3_1_2015'] +financials.loc[x,'3_8_2015']

    post_total_transactions_count = financials.loc[x,'3_15_2015'] + financials.loc[x,'3_22_2015'] +\
                                    financials.loc[x,'3_29_2015'] + \
    financials.loc[x, '4_5_2015'] +financials.loc[x,'4_12_2015'] +financials.loc[x,'4_19_2015'] +\
                                    financials.loc[x,'4_26_2015'] + \
    financials.loc[x, '5_3_2015'] +financials.loc[x,'5_10_2015'] +financials.loc[x,'5_17_2015'] + \
    financials.loc[x, '5_24_2015'] +financials.loc[x,'5_31_2015'] +financials.loc[x,'6_7_2015']

    avg_pre_total_transactions_count = pre_total_transactions_count / 13
    avg_post_total_transactions_count = post_total_transactions_count / 13

    growth_transaction_count = (financials.loc[x,'3_15_2015'] - financials.loc[x,'3_8_2015']) / \
                               financials.loc[x,'3_8_2015']

    financials.loc[x,'growth_transaction_count'] = growth_transaction_count

for y,storemasterrow in storemaster.iterrows():
    type = ""
    associates_poh_post = storemaster.loc[y,'associates_poh_post']
    close_time_post = storemaster.loc[y,'close_time_post']
    population_within_5 = storemaster.loc[y,'population_within_5']
    competition_within_5 = storemaster.loc[y,'competition_within_5']
    if (storemaster.loc[y,'type'] == "Standalone"):
        type = 1
    elif (storemaster.loc[y,'type'] == "Strip Mall"):
        type = 0
    storemaster.loc[y,'type'] = type
    storemaster.loc[y,'dummy_associates_poh_post'] = associates_poh_post * type
    storemaster.loc[y,'dummy_close_time_post'] = close_time_post * type
    storemaster.loc[y,'dummy_population_within_5'] = population_within_5 * type
    storemaster.loc[y,'dummy_competition_within_5'] = competition_within_5 * type

# Sorts through data for multiple regression analysis
combined=[]
for x,financialsrow2 in financials.iterrows():
    combined.append([financials.loc[x,'growth_transaction_count'],storemaster.loc[x,'associates_poh_post'],
                     storemaster.loc[x,'close_time_post'],storemaster.loc[x,'population_within_5'],
                     storemaster.loc[x,'competition_within_5'],
                     storemaster.loc[x,'dummy_associates_poh_post'],
                     storemaster.loc[x, 'dummy_close_time_post'],storemaster.loc[x,'dummy_population_within_5'],
                     storemaster.loc[x, 'dummy_competition_within_5'],storemaster.loc[x, 'type']])

np_combined = np.array(combined)
y1 = np_combined[:,0].astype(np.float)
x1 = np_combined[0:,1:10].astype(np.float)
x1 = sm.add_constant(x1)

# Creates multiple regression model and outputs results to text file
model3 = sm.OLS (y1,x1).fit()
text_file = open(outputDirectory + "mr_model.txt", "w")
text_file.write(str(model3.summary()))
