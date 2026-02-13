import pytest
import time
from httpx import AsyncClient, ASGITransport
from products_api.app import app

@pytest.mark.asyncio
async def test_products_stats_calculation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Usando timestamp para garantir nomes únicos e evitar IntegrityError
        ts = int(time.time())
        test_data = [
            {"name": f"Prod A {ts}", "price": 100.00, "description": "desc"},
            {"name": f"Prod B {ts}", "price": 200.00, "description": "desc"},
            {"name": f"Prod C {ts}", "price": 300.00, "description": "desc"},
        ]
        
        for item in test_data:
            await ac.post("/api/v1/products/", json=item)

        response = await ac.get("/api/v1/products/stats")
        assert response.status_code == 200
        data = response.json()
        
        # Validações
        assert data["total_count"] >= 3
        assert float(data["average_price"]) >= 100.00
