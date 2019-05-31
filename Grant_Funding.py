
"""
Created on Wed May 29 14:41:22 2019

@author: alyssa rose

Objective: determine areas that can best be benefitted from
getting grant money to improve infrastructure in the regions that 
are the lowest income and in states that have the worst infrastructure
ratings from data provided by ASCE
"""

import pandas as pd

# getting the poverty data
data = pd.read_csv('PovertyEstimates.csv')
# cleaning the data
data = data.rename(columns=data.iloc[2])
data = data.iloc[3:len(data), :]
data = data.drop(["Rural-urban_Continuum_Code_2003", "Urban_Influence_Code_2003",
                  "Rural-urban_Continuum_Code_2013", "Urban_Influence_Code_2013"], axis = 1)
us_totals = data.iloc[0, :]
data = data.iloc[1:len(data), :]



states = []
def state_totals(data):
    state = "Word"
    for i in range(len(data)):
        if data.iloc[i, 1] != state:
            states.append(data.iloc[i, :])
            state = data.iloc[i,1]

state_totals(data)

data.to_csv(r'C:\Users\alyss\OneDrive\Documents\Projects\Grant_Funding\PovertyEstimatesFix.csv')



"""
web scraping for the infrastructure grades
"""
from bs4 import BeautifulSoup
import requests
from csv import writer

state_names = pd.read_csv('states.csv')
state_names = state_names.drop('Abbreviation', axis = 1)
state_name_list = []
for i in range(len(state_names)):
    state_name_list.append(state_names.iloc[i,0])

# Purpose: func to get labels of graded things
# Input: empty list to store indices, name list of
#   things graded
# Returns: indices of the desired attributes
def get_labels(ind, name):
    labels = []
    for names in name:
        label = names.get_text().replace('\n', '')
        labels.append(label)
    #ind.append(labels.index('Bridges'))
    #ind.append(labels.index('Dams'))
    if not labels:
        ind.append(0)
    else:
        if 'Drinking Water' not in labels:
            ind.append(labels.index('Water and Wastewater'))
        else:
            ind.append(labels.index('Drinking Water'))
        if 'Roads' not in labels:
            ind.append(labels.index('Highways and Roads'))
        else:
            ind.append(labels.index('Roads'))
    return ind

# Purpose: func to get scores of desired labels
# Input: empty list to store scores, grade list of
#   things graded
# Returns: scores of the desired attributes
def get_scores(scores, grade):
    for grades in grade:
        score = grades.get_text().replace('\n', '')
        scores.append(score)
    return scores

state_name_list[state_name_list.index('District of Columbia')] = 'District-of-Columbia'
state_name_list[state_name_list.index('New Hampshire')] = 'New-Hampshire'
state_name_list[state_name_list.index('New Jersey')] = 'New-Jersey'
state_name_list[state_name_list.index('New Mexico')] = 'New-Mexico'
state_name_list[state_name_list.index('New York')] = 'New-York'
state_name_list[state_name_list.index('North Carolina')] = 'North-Carolina'
state_name_list[state_name_list.index('North Dakota')] = 'North-Dakota'
state_name_list[state_name_list.index('Rhode Island')] = 'Rhode-Island'
state_name_list[state_name_list.index('South Carolina')] = 'South-Carolina'
state_name_list[state_name_list.index('South Dakota')] = 'South-Dakota'
state_name_list[state_name_list.index('West Virginia')] = 'West-Virginia'

    
with open('stateInfra.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    header = ['State', 'Overall', 'Drinking Water','Roads']
    csv_writer.writerow(header)
    for i in state_name_list:
        response = requests.get('https://www.infrastructurereportcard.org/state-item/' 
                                + i +'/')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find_all(class_ = "e-name")
        grade = soup.find_all(class_ = "e-grade")
        
        # getting the indices of the desired labels
        ind = []
        ind = get_labels(ind, name)
        
        if len(ind) == 1:
            Overall = '0'
            Drinking_Water = '0'
            Roads = '0'
        # getting the scores of the desired attributes
        else:
            scores = []
            scores = get_scores(scores,grade)
            
            Overall = scores[0]
            
            scores = scores[1:len(scores)-1]
            #Bridges = scores[ind[0]]
            #Dams = scores[ind[1]]
            Drinking_Water = scores[ind[0]]
            Roads = scores[ind[1]]
        
        csv_writer.writerow([i, Overall, Drinking_Water, Roads])

