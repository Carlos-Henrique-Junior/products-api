from fastapi import FastAPI
from products_api.routers import products, auth

app = FastAPI(title="Products Management API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])

@app.get("/health_check")
def health_check():
    return {"status": "ok"}
