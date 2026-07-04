from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.limiter import limiter
from .db.init_db import init_db
from .api.routes.cases import router as cases_router
from .api.routes.users import router as users_router
from .api.routes.tags import router as tags_router
from .api.routes.case_notes import router as case_notes_router
from .api.routes.chain_of_custody import router as chain_of_custody_router
from .api.routes.evidence_item import router as evidence_item_router
from app.api.routes.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Case Management DF")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://case-df.local:8443", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.ENV == "development":
    from .db.seed import seed_db
    seed_db()

init_db()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(login_router, prefix="/api")
app.include_router(cases_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(case_notes_router, prefix="/api")
app.include_router(chain_of_custody_router, prefix="/api")
app.include_router(evidence_item_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "running"}

if __name__ == "__main__":
    import uvicorn

    ssl_kwargs = {}
    if settings.USE_HTTPS:
        ssl_kwargs = {
            "ssl_keyfile": settings.SSL_KEYFILE,
            "ssl_certfile": settings.SSL_CERTFILE,
        }

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        **ssl_kwargs,
    )