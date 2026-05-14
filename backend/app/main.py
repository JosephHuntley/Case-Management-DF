from fastapi import FastAPI

app = FastAPI(title="Case Management DF")


@app.get("/")
def root():
    return {"status": "running"}