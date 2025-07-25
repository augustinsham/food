from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from typing import Literal
import pandas as pd

ml=joblib.load("food_model.pkl")
label=joblib.load("label_encoders.pkl")

class inp_data(BaseModel):
    mood:Literal["happy","sad","neutral","bored","energetic","stressed","angry","excited","tired"]
    time_of_day:Literal["breakfast","dinner","lunch","evening"]
    is_hungry:Literal[0,1]
    prefers_spicy:Literal[0,1]
    diet:Literal["veg","non-veg","vegan"]

app=FastAPI()

@app.get('/')
def root_msg():
    return {"message":"welcome "}

@app.post('/predict')
def prediction(data:inp_data):
    inputs=pd.DataFrame([data.dict()])
    encode_columns = ["mood", "time_of_day", "diet"]

    for col in encode_columns:
        inputs[col] = label[col].transform(inputs[col])
    res=ml.predict(inputs)
    prd=label["food_prediction"].inverse_transform([res])[0]

    return {"Predicted_food":prd}

