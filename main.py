from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.config import API_HOST, API_PORT, API_VERSION
from api.api import api_router
from prometheus_fastapi_instrumentator import Instrumentator

origins = [
    "http://127.0.0.1:" + str(API_PORT),
    "http://localhost:" + str(API_PORT),
]

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Stock API - API with Prisma",
    description="Resources to CRUD by categories and products",
    summary="Stock API Project used FastAPI",
    version="1.0.0",
    terms_of_service="http://example.com/terms",
    contact={
        "name": "Gabriel B. Alves",
        "url": "http://github.com/gbalves1989",
        "email": "gbalves1989@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/" + API_VERSION)

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        log_level="info",
        reload=True
    )
