from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/") # a decorator to define a GET endpoint at the root URL
def home(): #this function handles requests to the root URL - not using async for simplicity
    return {"message": "Hello World"} # Simple GET endpoint returning a greeting message

