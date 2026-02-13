# 📦 Products Management API (Modern FastAPI)

![CI Status](https://github.com/SEU_USUARIO/products-api/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Standard-009688)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

API robusta para gerenciamento de produtos, desenvolvida com foco em alta performance, código limpo e análise de dados.

## 🛠 Tecnologias Utilizadas
* **Python 3.12/3.13**
* **FastAPI Standard**
* **SQLAlchemy Async**
* **SQLite (aiosqlite)**
* **Docker & Docker Compose**
* **Alembic** (Migrações)
* **Pytest & Coverage** (100% de cobertura)
* **GitHub Actions** (CI/CD)

## 📊 Analytics Integration
A API possui uma rota especializada (`/stats`) que utiliza funções agregadas do SQL para fornecer insights imediatos, ideais para integração com dashboards de **Power BI**.

## 🚀 Como Executar

### Via Docker (Recomendado)
```bash
docker compose up --build
```
Acesse a documentação interativa em: http://localhost:8000/docs

### Rodando Testes e Cobertura
```bash
poetry run pytest --cov=products_api --cov-report=html
```

## 📌 Métodos Implementados
* **GET**: Listagem e visualização.
* **POST**: Criação de recursos.
* **PUT/PATCH**: Atualização total e parcial.
* **DELETE**: Remoção de itens.
* **HEAD/OPTIONS**: Infraestrutura e metadados.

---
Desenvolvido por Carlos - Foco em Backend Python & Data Analysis.
