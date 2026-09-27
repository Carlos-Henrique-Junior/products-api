import time

import pytest
from httpx import ASGITransport, AsyncClient

from products_api.app import app


@pytest.mark.asyncio
async def test_products_stats_calculation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Usando timestamp para garantir nomes únicos e evitar IntegrityError
        ts = int(time.time())
        test_data = [
            {"name": f"Prod A {ts}", "price": 100.00, "description": "desc"},
            {"name": f"Prod B {ts}", "price": 401.00, "description": "desc"},
            {"name": f"Prod C {ts}", "price": 300.00, "description": "desc"},
        ]

        for item in test_data:
            response = await ac.post("/api/v1/products/", json=item)
            assert response.status_code == 201

        # Sem token o acesso é negado
        response = await ac.get("/api/v1/products/stats")
        assert response.status_code == 401

        # Com token as estatísticas refletem os produtos criados
        signup = await ac.post(
            "/auth/signup",
            json={"username": "analyst", "password": "secret123"},
        )
        assert signup.status_code == 201

        login = await ac.post(
            "/auth/token",
            data={"username": "analyst", "password": "secret123"},
        )
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await ac.get("/api/v1/products/stats", headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data["total_count"] == 3
        assert float(data["average_price"]) == 267.00
        assert float(data["min_price"]) == 100.00
        assert float(data["max_price"]) == 401.00
