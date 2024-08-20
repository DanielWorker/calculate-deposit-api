import uvicorn
from fastapi import FastAPI

from .api.deposit_api import DepositApi

app = FastAPI()

app.include_router(DepositApi)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
