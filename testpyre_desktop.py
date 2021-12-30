# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 10:28:53 2021

@author: jeroe
"""

import pyrebase
import streamlit as st
from matlab_integration_desktop import Matlab_Calc
from PIL import Image

img = Image.open(r"C:\Users\jeroe\OneDrive - TU Eindhoven\Vakken\Digital Twin 2\Matlab EDES python\Final version logo.png")
st.set_page_config(page_title='MySugarFlow', page_icon=img)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

food_1 = {}
food_2 = {}
food_3 = {}
food_4 = {}
food_5 = {}
food_6 = {}
food_7 = {}
food_8 = {}

food_1["banana"] = 22.84
food_2["apple"] = 13.81
food_3["tagliatelle"] = 79.26
food_4["cucumber"] = 3.00
food_5["white bread"] = 51.80
food_6["milk chocolate"] = 59.4
food_7["egg"] = 0.77
food_8["cheese"] = 5.77 

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

st.sidebar.image(img)

st.sidebar.title("MySugarFlow")

choice = st.sidebar.selectbox('login/signup',['Login','Sign up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password (at least 6 characters)', type = 'password')

if choice == 'Sign up':
    password_verify = st.sidebar.text_input('Please verify your password (at least 6 characters)', type = 'password')
    if password != password_verify:
        st.error("Your password and password verification don't match")
    elif password == password_verify:    
        handle = st.sidebar.text_input('Please input your app username')
        submit = st.sidebar.button('Create my account')
    
        if submit:
            user = auth.create_user_with_email_and_password(email,password)
            st.success('Your account has been created successfully')
            st.balloons()
            
            user = auth.sign_in_with_email_and_password(email,password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            db.child(user['localId']).child("Food").child("banana").set(food_1)
            db.child(user['localId']).child("Food").child("apple").set(food_2)
            db.child(user['localId']).child("Food").child("tagliatelle").set(food_3)
            db.child(user['localId']).child("Food").child("cucumber").set(food_4)
            db.child(user['localId']).child("Food").child("white bread").set(food_5)
            db.child(user['localId']).child("Food").child("milk chocolate").set(food_6)
            db.child(user['localId']).child("Food").child("egg").set(food_7)
            db.child(user['localId']).child("Food").child("cheese").set(food_8)
            st.title('Welcome '+handle)
            st.info('Login via login option')
        
data_pd = {}
weight_var = 0

#if "load_state" not in st.session_state:
#    st.session_state["load_state"] = False



if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login: 
        #st.session_state["load_state"] = True
        user = auth.sign_in_with_email_and_password(email,password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
        bio = st.radio('Choose an option:',['Home','Add food','Pick food','Base settings','Info about diabetes','About us'])
        if bio == 'Base settings':
            if db.child(user['localId']).child("Weight").get().val() is not None:
                st.write("Your last weight input was "+str(db.child(user['localId']).child("Weight").get().val())+" kg")
            if db.child(user['localId']).child("Weight").get().val() is not None:
                weight_var = db.child(user['localId']).child("Weight").get().val()
            weight = st.number_input('Please enter your bodyweight (in kg)')
            weight_button = st.button('Submit!')
            if weight_button and weight != 0:
                if weight_var>weight:
                    st.success("Great job!")
                db.child(user['localId']).child("Weight").set(weight)
                st.success('Your weight has been added successfully')
        elif bio == 'Home':
            st.header("Welcome to sugar flow")
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
                Add_food = st.checkbox("Add second food item")
                if Select_food and weight_1 != None:
                    carb_100 = db.child(user['localId']).child("Food").child(Chosen_food).get().val()
                    carbs = ((((carb_100[Chosen_food])/100)*1000)*Amount_food)
                    Test_1 = Matlab_Calc(amount_of_peoples, weight_1, carbs, time)
                    if Test_1 == 'YES GOOD YES EAT':
                        st.success("You can eat "+str(Amount_food)+" grams of "+Chosen_food)
                    else:
                        st.error("You cannot eat "+str(Amount_food)+" grams of "+Chosen_food)
                if Add_food:
                    Chosen_food_1 = st.selectbox("Select second food you want to eat",data_pd_1)
                    Amount_food_1 = st.number_input("grams of "+Chosen_food_1+" you want to eat ")
                    Select_food_1 = st.button("Calculate first and second food items")
                    Add_food_1 = st.checkbox("Add third food item")
                    if Select_food_1 and weight_1 != None:
                        carb_100 = db.child(user['localId']).child("Food").child(Chosen_food).get().val()
                        carb_100_1 = db.child(user['localId']).child("Food").child(Chosen_food_1).get().val()
                        carbs_1 = (((((carb_100_1[Chosen_food_1])/100)*1000)*Amount_food_1)+((((carb_100[Chosen_food])/100)*1000)*Amount_food))
                        Test_1_1 = Matlab_Calc(amount_of_peoples, weight_1, carbs_1, time)
                        if Test_1_1 == 'YES GOOD YES EAT':
                            st.success("You can eat "+str(Amount_food)+" grams of "+Chosen_food+" and "+str(Amount_food_1)+" grams of "+Chosen_food_1)
                        else:
                            st.error("You cannot eat "+str(Amount_food)+" grams of "+Chosen_food+" and "+str(Amount_food_1)+" grams of "+Chosen_food_1)
                    if Add_food_1:
                        Chosen_food_2 = st.selectbox("Select third food you want to eat",data_pd_1)
                        Amount_food_2 = st.number_input("grams of "+Chosen_food_2+" you want to eat  ")
                        Select_food_2 = st.button("Calculate all food items")
                        if Select_food_2 and weight_1 != None:
                            carb_100 = db.child(user['localId']).child("Food").child(Chosen_food).get().val()
                            carb_100_1 = db.child(user['localId']).child("Food").child(Chosen_food_1).get().val()
                            carb_100_2 = db.child(user['localId']).child("Food").child(Chosen_food_2).get().val()
                            carbs_2 = (((((carb_100_1[Chosen_food_1])/100)*1000)*Amount_food_1)+((((carb_100[Chosen_food])/100)*1000)*Amount_food)+((((carb_100_2[Chosen_food_2])/100)*1000)*Amount_food_2))
                            Test_1_2 = Matlab_Calc(amount_of_peoples, weight_1, carbs_2, time)
                            if Test_1_2 == 'YES GOOD YES EAT':
                                st.success("You can eat "+str(Amount_food)+" grams of "+Chosen_food+" and "+str(Amount_food_1)+" grams of "+Chosen_food_1+" and "+str(Amount_food_2)+" grams of "+Chosen_food_2)
                            else:
                                st.error("You cannot eat "+str(Amount_food)+" grams of "+Chosen_food+" and "+str(Amount_food_1)+" grams of "+Chosen_food_1+" and "+str(Amount_food_2)+" grams of "+Chosen_food_2)
                                           
            elif db.child(user['localId']).child("Food").get().val() is None and db.child(user['localId']).child("Weight").get().val() is not None:
                st.info('Please add food')
            elif db.child(user['localId']).child("Weight").get().val() is None and db.child(user['localId']).child("Food").get().val() is not None :
                st.info('Please add your weight in the base settings')
            elif db.child(user['localId']).child("Weight").get().val() is None and db.child(user['localId']).child("Food").get().val() is None:
                st.info('Please add your weight in the base settings')
                st.info('Please add food')
        elif bio == 'Info about diabetes':
            st.header("Diabetes")
            st.write("Diabetes is a disease in which the body can no longer balance blood sugar. The body has too little insulin or no longer makes insulin at all and often the reaction that the body should have to insulin is disturbed; cells in the body are then resistant to insulin. Insulin is a hormone that regulates blood sugar levels by lowering blood sugar levels. Due to the insulin shortage, there is too much sugar in the blood and high blood sugar levels for a long time causes damage to the heart, eyes, kidneys and feet. There are different types of diabetes. The most common form is type 2 diabetes in which there is too little insulin, and the body no longer responds properly to insulin. In type 1 diabetes, the immune system attacks the cells that make insulin: the beta cells in the pancreas. As a result, these cells can no longer produce insulin.")
            st.write("The following symptoms are common in type 2 diabetes: ")
            st.write("·More urination than usual, especially at night ")
            st.write("·Constant thirst  ")
            st.write("·Being very tired  ")
            st.write("·Losing weight unexpectedly  ")
            st.write("·Wounds that take longer to heal  ")
            st.write("·Impaired vision, such as red and burning eyes, blurred vision, double vision or poor vision")
            st.write("·Shortness of breath or leg pain when walking")
            st.write("·Infections that come back, such as cystitis")
            st.write("Type 1 diabetes is unfortunately not yet curable; people with type 1 diabetes should measure blood sugar, inject insulin or wear a pump every day. ")
            st.write("The first step in treating type 2 diabetes is living healthy:  ")
            st.write("·Eating healthy ")
            st.write("·Moving a lot  ")
            st.write("·Losing weight in case of overweight ")
            st.write("·Sufficient relaxation and sleeping enough ")
            st.write("·Quiting smoking  ")
            st.write("By living a healthy life, the average blood sugar level can go down and there is a chance that fewer or no medications for diabetes are needed. ")
            st.header("Prediabetes")
            st.write("Prediabetes is a major risk factor for developing type 2 diabetes; about 70% of people with prediabetes eventually develop diabetes. In prediabetes, the reaction to high blood sugar levels is already disturbed, but not so badly that diabetes is detected. It is essential that blood sugar levels are kept within normal values to prevent the further development of diabetes.  ")
            st.write("Type 2 diabetes is often asymptotic in the initial stages and can go unnoticed for years. Early diagnosis for the disease is important, because careful management can prevent long-term conditions. Impaired glucose tolerance is an indication of prediabetes and by means of an oral glucose tolerance test (OGTT), in which fasting 75 grams of sugar is consumed, prediabetes or diabetes can be determined. ")
            st.header("Diagnosis of diabetes")
            st.write("The most commonly used tests to diagnose diabetes are the fasting plasma glucose test (FPG) and the oral glucose tolerance test (OGTT). These tests both use the measurement of blood-glucose concentrations. Patients must be fasted before the study, so they are not allowed to eat anything from the night before on, so that nothing should be eaten at least 8 hours before the study. Another possibility is to use glycated hemoglobin (HbA1c) to check the average blood glucose levels over a longer period (2 to 3 months). The blood test measures what percentage of the total amount of hemoglobin (Hb) has changed to glycated hemoglobin (HbA1c). Because this glycated hemoglobin remains in the blood for an average of 6 to 8 weeks, it gives an impression of the average blood glucose level over that period. ")
            st.header("Movement recommendations")
            st.write("Exercise is important to be healthy. By exercising, the insulin sensitivity improves in diabetes, so that the blood sugar level becomes less high. In addition, exercise helps to get and stay fit, helps to maintain a healthy weight and works stress-reducing. At least half an hour of exercise a day is essential and the more, the better.   ")
            st.write("However, it is important to adjust medication or insulin to exercise. Due to the higher insulin sensitivity, there is a faster chance of low blood sugar (hypoglycemia). ")
            st.write("Ideas for movement: ")
            st.write("·A walk of 20 minutes or more  ")
            st.write("·Cycle through your neighborhood ")
            st.write("·Go for a run  ")
            st.write("·Work in the garden ")
            st.write("·Clean the house ")
            st.write("·Go swimming  ")
            st.write("Small things can already help in sitting less, such as walking to the grocery shop, dressing yourself standing, standing during cooking, taking the stairs instead of the lift. Try to stand up every half hour. ")
            st.write("Interesting facts: ")
            st.write("·Movement can reduce sleeping issues ")
            st.write("·Walking is good for your mood. Serotine, the happiness hormone, is released in the brain during movement, so try to move! ")
            
        elif bio == 'About us':
            st.header("About us")
            st.write("We are Charlie, Elena, Jeroen, Tessa and Sterre, together we form group 9 for the course USE Digital Twin in Healthcare at Eindhoven University of Technology. Together we have developed this User Interface to help people with prediabetes to inform them about their own disease and to be able to help with what is and is not wise to eat with the user's personal information.  ")
            st.write("The User Interface is still under development, but our vision is to be able to link the dashboard with a Continuous Glucose Monitor (CGM). The dashboard is connected to the Eindhoven Diabetes Education Simulator, eDES, which is a physiologically-based mathematical model. Through the CGM, eDES can check whether the glucose value does not become too high by eating a certain food. Based on the information of the model, the dashboard advises the user.  ")
            st.subheader("Contact")
            st.write("Do you have a question, complaint or compliment? We are happy to help you! We are available at the following email address: ")
            st.write("pentabetes@gmail.com ")
                    
        
    
