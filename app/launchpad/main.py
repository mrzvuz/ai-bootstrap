from fastapi import FastAPI
from launchpad.api.router import router as process_router

app = FastAPI()
app.include_router(process_router)
