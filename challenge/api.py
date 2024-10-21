import fastapi
from fastapi import HTTPException
import pandas as pd

#from model import DelayModel

from challenge.model import DelayModel

#from src.api.schema.predict import ModelInput 

from challenge.src.api.schema.predict import ModelInput 

app = fastapi.FastAPI()
model = DelayModel()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(data: ModelInput) -> dict:
    #data = data.model_dump()
    data = data.dict()
    
    input_data = pd.DataFrame(data['flights'])
    preprocess_output = model.preprocess(data = input_data)

    if not isinstance(preprocess_output, pd.DataFrame):
        raise HTTPException(status_code=400, detail=preprocess_output)

    predictions_output = model.predict(features = preprocess_output)

    if not isinstance(predictions_output, list):
        raise HTTPException(status_code=400, detail=predictions_output)
    
    return {"predict": predictions_output}