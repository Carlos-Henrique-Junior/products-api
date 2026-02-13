import pytest
from httpx import AsyncClient, ASGITransport
from products_api.app import app

@pytest.mark.asyncio
async def test_full_http_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        # 1. POST: Criar um produto
        new_product = {"name": "Monitor Gamer", "price": 1200.50, "description": "144hz IPS"}
        response = await ac.post("/api/v1/products/", json=new_product)
        assert response.status_code == 201
        product_id = response.json()["id"]

        # 2. GET: Listar
        response = await ac.get("/api/v1/products/")
        assert response.status_code == 200
        assert any(p["id"] == product_id for p in response.json()["products"])

        # 3. HEAD: Verificar sem corpo
        response = await ac.head(f"/api/v1/products/{product_id}")
        assert response.status_code == 200
        assert response.text == ""

        # 4. PUT: Atualização total
        updated_total = {"name": "Monitor UltraWide", "price": 1500.00, "description": "34 polegadas"}
        response = await ac.put(f"/api/v1/products/{product_id}", json=updated_total)
        assert response.status_code == 200

        # 5. PATCH: Atualização parcial
        response = await ac.patch(f"/api/v1/products/{product_id}", json={"price": 1300.00})
        assert response.status_code == 200
        assert float(response.json()["price"]) == 1300.00

        # 6. OPTIONS: Métodos permitidos
        response = await ac.options("/api/v1/products/")
        assert response.status_code == 200
        assert "GET" in response.headers["allow"]

        # 7. DELETE: Remover
        response = await ac.delete(f"/api/v1/products/{product_id}")
        assert response.status_code == 204
