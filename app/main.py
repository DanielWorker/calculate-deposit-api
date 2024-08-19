import uvicorn
from fastapi import FastAPI
from app.routers.DepositRouter import DepositRoter


app = FastAPI()

app.include_router(DepositRoter)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
