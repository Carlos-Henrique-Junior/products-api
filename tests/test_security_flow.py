import pytest
from httpx import AsyncClient, ASGITransport
from products_api.app import app

@pytest.mark.asyncio
async def test_full_secure_analytics_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        # 1. Signup: Criar um usuário de teste
        user_data = {"username": "testuser", "password": "testpassword"}
        signup_res = await ac.post("/auth/signup", json=user_data)
        assert signup_res.status_code == 201

        # 2. Login: Obter o token JWT
        login_data = {"username": "testuser", "password": "testpassword"}
        login_res = await ac.post("/auth/token", data=login_data)
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # 3. Proteção: Tentar acessar /stats SEM token (Deve dar 401)
        forbidden_res = await ac.get("/api/v1/products/stats")
        assert forbidden_res.status_code == 401

        # 4. Acesso: Tentar acessar /stats COM token (Deve dar 200)
        headers = {"Authorization": f"Bearer {token}"}
        secure_res = await ac.get("/api/v1/products/stats", headers=headers)
        assert secure_res.status_code == 200
        
        data = secure_res.json()
        assert "total_count" in data
