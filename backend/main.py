from fastapi import FastAPI
from app.db.init_db import init_db

app = FastAPI(title="Case Management DF")

init_db()

@app.get("/")
def root():
    return {"status": "running"}