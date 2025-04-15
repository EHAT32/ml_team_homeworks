from fastapi import FastAPI, Request, HTTPException
import pickle 
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

with open("Random_Forest.pkl", "rb") as f:
    model = pickle.load(f)
    
#счётчик запросов
request_count = 0

def encode_vehicle_age(age):
    if age < 1:
        return 0
    elif 1 <= age <= 2:
        return 1
    else:
        return 2

def load_policy_labels(path="channel_modes.txt"):
    with open(path, "r") as file:
        labels = file.readline().strip().split(" ")
        labels = [int(l) for l in labels]
    return labels

def encode_policy_channel(val):
    label_pos = load_policy_labels()
    dist = np.array(label_pos, copy=True)
    dist = np.abs(dist - val)
    return np.argmin(dist)
    

class PredictionInput(BaseModel):
    Previously_Insured : bool
    Vehicle_Age : int
    Vehicle_Damage : bool
    Policy_Sales_Channel : int
    
@app.get("/stats")
def stats():
    return {"request_count":request_count}

@app.get("/health")
def health():
    return {"status":"OK"}

@app.post("/predict_model")
def predict_model(input_data : PredictionInput):
    global request_count
    request_count += 1
    
    #Оборачиваем данные в df, преобразуем их
    new_data = pd.DataFrame({
        "Previously_Insured" : int(input_data.Previously_Insured),
        "Vehicle_Age" : encode_vehicle_age(input_data.Vehicle_Age),
        "Vehicle_Damage" : int(input_data.Vehicle_Damage),
        "Policy_Sales_Channel" : encode_policy_channel(input_data.Policy_Sales_Channel),
    }, index=[0])
    
    #предсказание
    predictions = model.predict(new_data)
    
    #интерпретация данных
    result = "Клиент возьмёт страховку" if predictions[0] == 1 else "Клиент не возьмёт страховку"
    
    return {"prediction" : result}

'''
Проверка работы API (/health)
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d '{"Previously_Insured": true, "Vehicle_Age": 3, "Vehicle_Damage": false, "Policy_Sales_Channel": 100}'
'''

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)