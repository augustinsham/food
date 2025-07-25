import streamlit as st
import pymongo
import requests

client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["Food_prediction"]
collection=db["users"] 

st.title("🍽️ Food Predictor😋 ")
select=st.sidebar.selectbox("Page Navigator",["Registeration Page","Prediction Page"])

if(select=="Registeration Page"):
    st.header("New Registration")
    un=st.text_input("Username :")
    pw=st.text_input("Password :",type="password")
    btn=st.button("Register")
    if btn:
        if un!="" and pw!="":
            collection.insert_one({
            "Username":un,
            "Password":pw
            })
            st.success("New User Registered!!")
        else:
            st.error("Enter the proper username and password")

elif(select=="Prediction Page"):    
    st.header("Login ")
    un=st.text_input("Username: ")
    pw=st.text_input("Password",type="password")
    if un!="" and pw!="":
        if(collection.find_one({"Username":un,"Password":pw}) is not None):
            st.markdown("------------------")
            st.header(f"Hi {un} Predict your food preference")
            mood=st.selectbox("Mood :",["happy","sad","neutral","bored","energetic","stressed","angry","excited","tired"])
            time_of_day=st.selectbox("time_of_day",["breakfast","dinner","lunch","evening"])
            diet=st.selectbox("Choose your diet :",["veg","non-veg","vegan"])
            is_hungry=st.checkbox("Are You Hungry ?")
            ps=st.checkbox("Prefer Spicy ! ")

            if(st.button("Predict the Food")):
                data={
                    "mood":mood,
                    "time_of_day":time_of_day,
                    "is_hungry":is_hungry,
                    "prefers_spicy":ps,
                    "diet":diet
                }
                res=requests.post("http://127.0.0.1:8000/predict",json=data)
                result=res.json()
                st.write("Predicted Food : ",result["Predicted_food"])
