from __future__ import annotations

from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.api import auth as auth_router
from app.api import users as users_router
from app.api import news as news_router
from app.api import documents as documents_router
from app.init_db import init_db


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Корпоративный портал с системой авторизации. "
        "Поддерживает три роли пользователей: сотрудник, HR-менеджер, администратор."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Ошибка валидации входных данных",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера. Обратитесь к администратору."},
    )


app.include_router(auth_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(news_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(documents_router.router, prefix=settings.API_V1_PREFIX)


@app.get("/api/health", tags=["Служебные"])
def health() -> Dict[str, str]:
    return {"status": "ok", "service": settings.PROJECT_NAME}


FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    def root_index() -> FileResponse:
        return FileResponse(str(FRONTEND_DIR / "pages" / "login.html"))

    @app.get("/{page_name}.html", include_in_schema=False)
    def serve_page(page_name: str) -> FileResponse:
        page_path = FRONTEND_DIR / "pages" / f"{page_name}.html"
        if page_path.exists():
            return FileResponse(str(page_path))
        raise HTTPException(status_code=404, detail="Страница не найдена")
