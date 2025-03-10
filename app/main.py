from fastapi import FastAPI
from api.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root(): 
    return {"message":"Email Automation API is running!"}

@app.get("/test")
def test_root():
    return {"message:": "Test Complete"}