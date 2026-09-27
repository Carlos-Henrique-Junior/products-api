
import requests

API_URL = "http://127.0.0.1:8000"

def populate():
    # 1. Criar o usuário principal
    user_data = {"username": "carlos", "password": "123"}
    requests.post(f"{API_URL}/auth/signup", json=user_data)
    print("✅ Usuário 'carlos' criado (ou já existente).")

    # 2. Login para pegar o token (necessário para o /stats se quisermos testar)
    # Mas aqui vamos cadastrar os produtos que são rotas abertas no momento
    products = [
        ("Cadeira Gamer", 1500.00), ("Mouse Pad RGB", 120.00), 
        ("Monitor 4K", 3200.00), ("Teclado Mecânico", 450.00),
        ("Headset 7.1", 280.00), ("Webcam Full HD", 350.00),
        ("Suporte Articulado", 180.00), ("Placa de Vídeo RTX", 4500.00),
        ("Memória RAM 16GB", 400.00), ("SSD 1TB NVMe", 550.00)
    ]

    for name, price in products:
        payload = {
            "name": name,
            "price": price,
            "description": f"Excelente {name.lower()} para o seu setup."
        }
        requests.post(f"{API_URL}/api/v1/products/", json=payload)
    
    print(f"🚀 {len(products)} produtos inseridos com sucesso!")

if __name__ == "__main__":
    try:
        populate()
    except Exception as e:
        print(f"❌ Erro ao conectar na API: {e}. Garanta que o Docker está rodando!")
