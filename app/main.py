import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/developer")
async def get_developer():
    return {"developer": os.getenv("DEVELOPER", "unknown")}
