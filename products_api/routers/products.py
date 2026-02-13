from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger
from decimal import Decimal
import jwt

from products_api.core.database import get_session
from products_api.core.security import SECRET_KEY, ALGORITHM
from products_api.models.products import Product
from products_api.schemas.products import (
    ProductSchema, ProductListPublicSchema, ProductPublicSchema,
    ProductUpdateSchema, ProductStatsSchema,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

# 1. ANALYTICS (Protegido para o Dashboard)
@router.get('/stats', response_model=ProductStatsSchema, summary='DASHBOARD: Estatísticas', tags=['Analytics'])
async def get_products_stats(db: AsyncSession = Depends(get_session), user: str = Depends(get_current_user)):
    logger.info(f"Usuário {user} acessando insights analíticos")
    query = select(func.count(Product.id), func.avg(Product.price), func.min(Product.price), func.max(Product.price))
    result = await db.execute(query)
    count, avg, min_p, max_p = result.fetchone()
    return {
        "total_count": count or 0,
        "average_price": round(Decimal(avg or 0), 2),
        "min_price": Decimal(min_p or 0),
        "max_price": Decimal(max_p or 0)
    }

# 2. LISTAR
@router.get('/', response_model=ProductListPublicSchema, summary='GET: Listar produtos')
async def list_products(db: AsyncSession = Depends(get_session)):
    result = await db.scalars(select(Product))
    return {'products': result.all()}

# 3. CRIAR
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductPublicSchema, summary='POST: Criar produto')
async def create_product(product: ProductSchema, db: AsyncSession = Depends(get_session)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# 4. ATUALIZAÇÃO TOTAL (PUT)
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

# 5. ATUALIZAÇÃO PARCIAL (PATCH)
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

# 6. EXCLUIR (DELETE)
@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, summary='DELETE: Excluir produto')
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await db.delete(product)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
