
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.exception_handlers import validation_exception_handler
from app.routers.employees import router as employees_router


app = FastAPI(
    title="Employee Directory API",
    description="Search employees by name or department.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.include_router(employees_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
