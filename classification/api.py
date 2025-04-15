from fastapi import FastAPI, Request, HTTPException
import pickle 
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

with open("Random_Forest.pkl", "rb") as f:
    model = pickle.load(f)
    
#счётчик запросов
request_count = 0

class PredictionInput(BaseModel):
    previously_insured : bool