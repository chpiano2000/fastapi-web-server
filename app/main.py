import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/developer")
async def get_developer():
    return {"developer": os.getenv("DEVELOPER", "unknown")}
