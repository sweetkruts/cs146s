from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router

app = FastAPI(title="Modern Software Dev Starter (Week 5)")

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Mount static frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"ok": False, "error": {"code": exc.status_code, "message": exc.detail}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"ok": False, "error": {"code": "VALIDATION_ERROR", "message": str(exc.errors())}},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"ok": False, "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}},
    )


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)
