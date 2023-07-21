from fastapi import FastAPI
import sys
sys.path.append("./..")
from bus_pred import *
from pydantic import BaseModel

app = FastAPI()

X_test = model_eval()
w_X_test = w_model_eval()

class week_time_IN(BaseModel):
    times: int
class week_time_Out(BaseModel):
    wtime: list

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pred")
def read_users():
    pred = np.round(model_pred(X_test)).astype(int).tolist()
    return {'pred' : pred}

@app.post("/w_pred", response_model = week_time_Out)
def read_users(times: week_time_IN):
    print(times)
    time_pred = []
    pred = np.round(w_model_pred(w_X_test)).astype(int).tolist()
    for i in range(times.times - 6, len(pred), 17):
        time_pred.append(pred[i])
    print(time_pred)
    return {'wtime' : time_pred}
