import uvicorn
from fastapi import FastAPI

from app.api.deposit_api import router as reposit_router
from app.api.user_api import router as user_router

app = FastAPI()

app.include_router(reposit_router)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
