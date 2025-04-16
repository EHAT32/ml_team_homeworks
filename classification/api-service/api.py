from fastapi import FastAPI, Request, HTTPException
import pickle 
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Загрузка модели из файла
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
    
# Счетчик запросов
request_count = 0

def encode_vehicle_age(age):
    if age == "< 1 Year":
        return 0
    elif age == "1-2 Year":
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
    
# Модель для валидации входных данных
class PredictionInput(BaseModel):
    Previously_Insured : bool
    Vehicle_Age : str
    Vehicle_Damage : bool
    Policy_Sales_Channel : int
    
# Батчи для тестирования модели
class BatchPredictionInput(BaseModel):
    data: list[PredictionInput]

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status":"OK"}

@app.post("/predict_model")
def predict_model(input_data : PredictionInput):
    global request_count
    request_count += 1
    
    # Оборачиваем данные в df, преобразуем их
    new_data = pd.DataFrame({
        "Previously_Insured" : int(input_data.Previously_Insured),
        "Vehicle_Age" : encode_vehicle_age(input_data.Vehicle_Age),
        "Vehicle_Damage" : int(input_data.Vehicle_Damage),
        "Policy_Sales_Channel" : encode_policy_channel(input_data.Policy_Sales_Channel),
    }, index=[0])
    
    # Предсказание
    predictions = model.predict(new_data)
    prediction_value = int(predictions[0])  
    
    # Интерпретация данных с проверкой
    try:
        result = ("Клиент не возьмёт страховку", "Клиент возьмёт страховку")[prediction_value]
    except IndexError:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction mapping error for value: {prediction_value}"
        )
    
    return {"prediction": result, "_original_prediction": prediction_value}
    
# Тест API
@app.post("/test_predict_batch")
def test_predict_batch(batch_data: BatchPredictionInput):
    global request_count
    request_count += len(batch_data.data)

    # Преобразуем данные в DataFrame
    new_data = pd.DataFrame([{
        "Previously_Insured": int(item.Previously_Insured),
        "Vehicle_Age": encode_vehicle_age(item.Vehicle_Age),
        "Vehicle_Damage": int(item.Vehicle_Damage),
        "Policy_Sales_Channel": encode_policy_channel(item.Policy_Sales_Channel)
    } for item in batch_data.data])
    
    # Преобразуем типы данных в DataFrame
    new_data = new_data.astype({
        "Previously_Insured": int,
        "Vehicle_Age": str,
        "Vehicle_Damage": int,
        "Policy_Sales_Channel": int
    })

    # Предсказания
    predictions = model.predict(new_data)
    # Преобразуем numpy array в list, а элементы numpy.int64 в int
    return {"predictions": [int(p) for p in predictions.tolist()]}


    
'''
Проверка работы API (/health)
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d '{"Previously_Insured": true, "Vehicle_Age": "1-2 Year", "Vehicle_Damage": false, "Policy_Sales_Channel": 100}'
'''

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)