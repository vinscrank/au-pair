from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import auth, discovery, profiles
from app.routers.profiles import UPLOAD_DIR
from app.vocab import meta

app = FastAPI(title="Au pair")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_handler(_request: Request, exc: RequestValidationError):
    message = "Check the form and try again."
    errors = exc.errors()
    if errors:
        message = str(errors[0].get("msg", message))
        prefix = "Value error, "
        if message.startswith(prefix):
            message = message[len(prefix) :]
    return JSONResponse(status_code=422, content={"detail": message})


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/meta")
def get_meta():
    return meta()


app.include_router(auth.router, prefix="/api")
app.include_router(profiles.router, prefix="/api")
app.include_router(discovery.router, prefix="/api")

UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
