from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.routes.cases import router as cases_router
from app.api.routes.users import router as users_router

app = FastAPI(title="Case Management DF")

init_db()

app.include_router(cases_router)
app.include_router(users_router)

@app.get("/")

def root():
    return {"status": "running"}