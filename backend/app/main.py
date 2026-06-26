from .db.seed import seed_db
from fastapi import FastAPI
from .db.init_db import init_db
from .api.routes.cases import router as cases_router
from .api.routes.users import router as users_router
from .api.routes.tags import router as tags_router
from .api.routes.case_notes import router as case_notes_router
from .api.routes.chain_of_custody import router as chain_of_custody_router
from .api.routes.evidence_item import router as evidence_item_router

app = FastAPI(title="Case Management DF")

init_db()
seed_db()

app.include_router(cases_router)
app.include_router(users_router)
app.include_router(tags_router)
app.include_router(case_notes_router)
app.include_router(chain_of_custody_router)
app.include_router(evidence_item_router)

@app.get("/")

def root():
    return {"status": "running"}