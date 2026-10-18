from fastapi import FastAPI
from ai_bootstrap.api.router import router as process_router

app = FastAPI()
app.include_router(process_router)
