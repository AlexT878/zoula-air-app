from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users
from app.core.lifespan import lifespan

app = FastAPI(title="Zoula Air API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Zoula Air API", "status": "Running", "docs": "/docs"}
