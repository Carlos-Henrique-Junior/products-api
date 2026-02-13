from fastapi import FastAPI, status
from products_api.routers import products

app = FastAPI(
    title="Products Management API",
    description="API robusta para gerenciamento de inventário de produtos com suporte total a métodos RESTful.",
    version="1.0.0",
    contact={
        "name": "Carlos",
        "url": "https://github.com/seu-usuario",
    },
    license_info={
        "name": "MIT",
    },
)

app.include_router(
    router=products.router,
    prefix='/api/v1/products',
    tags=['Products'], # Isso agrupa as rotas em uma seção no Swagger
)

@app.get('/health_check', status_code=status.HTTP_200_OK, tags=['System'])
def health_check():
    return {'status': 'ok'}
