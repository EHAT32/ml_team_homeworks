import pandas as pd
import requests
import pickle
import os
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

def decode_vehicle_age(label):
    ages = ["< 1 Year", "1-2 Year", "> 2 Years"]
    return ages[label]

# Пути к файлам
MODEL_PATH = os.path.join("api-service", "model.pkl")
TEST_DATA_PATH = "test_final.csv"
API_URL = "http://127.0.0.1:5000/test_predict_batch"  # URL для батчей

# Загрузка тестовых данных
print("Загрузка данных...")
row_num = 1000
data_test = pd.read_csv(TEST_DATA_PATH)#[:row_num]

# Разделение на X_test и y_test
tmp_X_test = data_test.drop(columns=['Response'])
X_test = tmp_X_test.copy()
y_test = data_test['Response'].copy()

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Прямое предсказание с использованием модели
print("Предсказание напрямую...")
y_pred_direct = model.predict(X_test)

# Предсказания через API
print("Предсказание через API...")
X_test["Vehicle_Age"] = X_test["Vehicle_Age"].apply(lambda x: decode_vehicle_age(x))
y_pred_api = []
batch_size = row_num  # Размер батча
for i in tqdm(range(0, len(X_test), batch_size), desc="Отправка батчей"):
    batch = X_test.iloc[i:i + batch_size].to_dict(orient='records')
    
    # Формируем JSON для запроса
    payload = {"data": batch}
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        predictions = response.json()["predictions"]
        y_pred_api.extend(predictions)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        y_pred_api.extend([None] * len(batch))  # Добавляем None для каждого элемента в батче


print("Метрики напрямую")
print(classification_report(y_test[:len(y_pred_api)], y_pred_api))
print("\nМетрики API:")
print(classification_report(y_test[:len(y_pred_api)], y_pred_api))
