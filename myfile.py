# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 09:07:55 2021

@author: Sterre de Lignie
"""

import streamlit as st
from matlab_integration_desktop import Matlab_Calc
import pandas as pd


Food_list = []
df1 = pd.DataFrame({"Food":Food_list})

st.title('Pentabetes diabetes tester biatch')
amount_of_peoples = 1
carbs = 0
weight = 0
time = 0

@st.cache(allow_output_mutation=True)
def get_data():
    return []


weight = st.number_input('weight (kg)')
Food_addition = st.text_input("Type the name of what food you want to add")
Carb_addition = st.number_input("Amount of carbohydrates per 100 grams of choosen food")
press_input = st.button("Add food")

if press_input and Carb_addition != 0:
    get_data().append({"Food": Food_addition, "Carbs": Carb_addition})
data_pd = pd.DataFrame(get_data())
if "Food" in data_pd:
    column_b = data_pd["Food"]
    Chosen_food = st.selectbox("Select food you want to eat",column_b)
    Amount_food = st.number_input("grams of food you want to eat")
    time = st.number_input('time of consumption (min)')
    Select_food = st.button("Calculate food")
    if Select_food and "Food" in data_pd:
        row_food = data_pd.loc[data_pd["Food"] == Chosen_food]
        carbs = ((((data_pd.loc[row_food.index[0]]["Carbs"])/100)*1000)*Amount_food)
        Test_1 = Matlab_Calc(amount_of_peoples, weight, carbs, time)
        st.write(Test_1)
        
            
    
    
    




