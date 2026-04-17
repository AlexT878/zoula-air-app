from fastapi import FastAPI
from app.core.lifespan import lifespan

app = FastAPI(title="Zoula Air API", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to Zoula Air API"}
