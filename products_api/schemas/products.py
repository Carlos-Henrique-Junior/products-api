from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class ProductSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: Decimal = Field(..., gt=0)
    description: str = Field(..., min_length=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Teclado Mecânico RGB",
                "price": 350.90,
                "description": "Teclado switch blue com layout ABNT2"
            }
        }
    )

class ProductPublicSchema(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    price: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1)

class ProductListPublicSchema(BaseModel):
    products: List[ProductPublicSchema]

# Novo Schema para Dados Analíticos
class ProductStatsSchema(BaseModel):
    total_count: int
    average_price: Decimal
    min_price: Decimal
    max_price: Decimal
