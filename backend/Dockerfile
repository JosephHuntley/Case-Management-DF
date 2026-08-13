# Place this file at: backend/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Build with --build-arg DEV_MODE=true to install requirements-dev.txt instead
ARG DEV_MODE=false

COPY requirements.txt requirements-dev.txt ./

RUN if [ "$DEV_MODE" = "true" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    else \
        pip install --no-cache-dir -r requirements.txt; \
    fi

COPY . .

EXPOSE 8000

# Matches your local "python -m app.main" workflow exactly.
# Assumes app/main.py calls uvicorn.run(..., host="0.0.0.0", port=8000) —
# if it binds to 127.0.0.1 it won't be reachable from outside the container.
CMD ["python", "-m", "app.main"]
