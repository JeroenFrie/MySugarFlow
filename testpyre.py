# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 10:28:53 2021

@author: jeroe
"""

import pyrebase
import streamlit as st
import pandas as pd
from matlab_integration_desktop import Matlab_Calc

amount_of_peoples = 1

firebaseConfig = {
  "apiKey": "AIzaSyCxJfOQVBDT3cck7kMKJyCBgK8cdLCkeUI",
  "authDomain": "test-fireestore-streamlit.firebaseapp.com",
  "projectId": "test-fireestore-streamlit",
  "databaseURL": "https://test-fireestore-streamlit-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "test-fireestore-streamlit.appspot.com",
  "messagingSenderId": "110694863664",
  "appId": "1:110694863664:web:03f705aa4e180ff7762ef5",
  "measurementId": "G-2F25EY60QH"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()
storage = firebase.storage()

st.sidebar.title("Our community app")

choice = st.sidebar.selectbox('login/signup',['Login','Sign up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type = 'password')

if choice == 'Sign up':
    handle = st.sidebar.text_input('Please input your app handle name', value = 'Default')
    submit = st.sidebar.button('Create my account')
    
    if submit:
        user = auth.create_user_with_email_and_password(email,password)
        st.success('Your account has been created successfully')
        st.balloons()
        
        user = auth.sign_in_with_email_and_password(email,password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome '+handle)
        st.info('Login via login option')
        
data_pd = {}

if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email,password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
        bio = st.radio('Choose an option:',['Home','Add food','Pick food','Base settings'])
        if bio == 'Base settings':
            weight = st.number_input('Please enter your bodyweight (in kg)')
            weight_button = st.button('Submit!')
            if weight_button and weight != 0:
                db.child(user['localId']).child("Weight").set(weight)
                st.success('Your weight has been added successfully')
        elif bio == 'Home':
            st.write("Welcome to the Pentabetes diabetes tester!!")
        elif bio == 'Add food':
            Food_addition = st.text_input("Type the name of what food you want to add")
            Carb_addition = st.number_input("Amount of carbohydrates per 100 grams of chosen food")
            press_input = st.button("Add food")
            if press_input and Carb_addition != 0:
                data_pd[Food_addition] = Carb_addition
                db.child(user['localId']).child("Food").child(Food_addition).set(data_pd)
                st.success('Your food has been added successfully')
        elif bio == 'Pick food':
            if db.child(user['localId']).child("Food").get().val() is not None and db.child(user['localId']).child("Weight").get().val() is not None:
                data_pd_1 = db.child(user['localId']).child("Food").get().val()
                weight_1 = db.child(user['localId']).child("Weight").get().val()
                Chosen_food = st.selectbox("Select food you want to eat",data_pd_1)
                Amount_food = st.number_input("grams of "+Chosen_food+" you want to eat")
                time = st.number_input('Time until consumption (min)')
                Select_food = st.button("Calculate food")
                if Select_food and weight_1 != None:
                    carb_100 = db.child(user['localId']).child("Food").child(Chosen_food).get().val()
                    carbs = ((((carb_100[Chosen_food])/100)*1000)*Amount_food)
                    Test_1 = Matlab_Calc(amount_of_peoples, weight_1, carbs, time)
                    st.write(Test_1)
            elif db.child(user['localId']).child("Food").get().val() is None and db.child(user['localId']).child("Weight").get().val() is not None:
                st.info('Please add food')
            elif db.child(user['localId']).child("Weight").get().val() is None and db.child(user['localId']).child("Food").get().val() is not None :
                st.info('Please add your weight in the base settings')
            elif db.child(user['localId']).child("Weight").get().val() is None and db.child(user['localId']).child("Food").get().val() is None:
                st.info('Please add your weight in the base settings')
                st.info('Please add food')
                
                
        
    
