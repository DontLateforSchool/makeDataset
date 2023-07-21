from fastapi import FastAPI
import sys
sys.path.append("./..")
from bus_pred import *
from pydantic import BaseModel

app = FastAPI()

X_test = model_eval()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pred")
def read_users():
    pred = np.round(model_pred(X_test)).astype(int).tolist()
    return {'pred' : pred}
