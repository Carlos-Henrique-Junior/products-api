from contextlib import asynccontextmanager

from fastapi import FastAPI

from products_api.core.database import engine
from products_api.models import Base
from products_api.routers import auth, products


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create the local schema when running without an external migration step."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Products Management API", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(
    products.router, prefix="/api/v1/products", tags=["Products"]
)


@app.get("/health_check")
def health_check():
    return {"status": "ok"}
