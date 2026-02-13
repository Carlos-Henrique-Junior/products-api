from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger
from decimal import Decimal

from products_api.core.database import get_session
from products_api.models.products import Product
from products_api.schemas.products import (
    ProductSchema,
    ProductListPublicSchema,
    ProductPublicSchema,
    ProductUpdateSchema,
    ProductStatsSchema,
)

router = APIRouter()

@router.get('/stats', response_model=ProductStatsSchema, summary='DASHBOARD: Estatísticas', tags=['Analytics'])
async def get_products_stats(db: AsyncSession = Depends(get_session)):
    logger.info("Calculando insights analíticos")
    query = select(func.count(Product.id), func.avg(Product.price), func.min(Product.price), func.max(Product.price))
    result = await db.execute(query)
    count, avg, min_p, max_p = result.fetchone()
    return {
        "total_count": count or 0,
        "average_price": round(Decimal(avg or 0), 2),
        "min_price": Decimal(min_p or 0),
        "max_price": Decimal(max_p or 0)
    }

@router.get('/', response_model=ProductListPublicSchema, summary='GET: Listar produtos')
async def list_products(db: AsyncSession = Depends(get_session)):
    result = await db.scalars(select(Product))
    return {'products': result.all()}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductPublicSchema, summary='POST: Criar produto')
async def create_product(product: ProductSchema, db: AsyncSession = Depends(get_session)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.put('/{product_id}', response_model=ProductPublicSchema, summary='PUT: Atualização total')
async def update_product_total(product_id: int, product_data: ProductSchema, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in product_data.model_dump().items():
        setattr(product, key, value)
    await db.commit()
    await db.refresh(product)
    return product

@router.patch('/{product_id}', response_model=ProductPublicSchema, summary='PATCH: Atualização parcial')
async def partial_update_product(product_id: int, product_update: ProductUpdateSchema, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    await db.commit()
    await db.refresh(product)
    return product

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, summary='DELETE: Excluir produto')
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await db.delete(product)
    await db.commit()
    return

@router.head('/{product_id}', summary='HEAD: Verificar recurso')
async def head_product(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        return Response(status_code=404)
    return Response(status_code=200)

@router.options('/', summary='OPTIONS: Métodos permitidos')
async def options_products():
    return Response(status_code=200, headers={"Allow": "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD"})
