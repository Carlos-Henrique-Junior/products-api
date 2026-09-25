# 📦 Products Management API (Modern FastAPI) & BI Dashboard

![CI Status](https://github.com/Carlos-Henrique-Junior/products-api/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.13-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![Coverage](https://img.shields.io/badge/coverage-78%25-green)

Sistema completo de gerenciamento de inventário com foco em **segurança**, **performance** e **análise de dados**. 

> ⚠️ **Projeto em Desenvolvimento**: Atualmente integrando módulos de exportação de dados e refinando o pipeline de CI/CD.

## 🛠 Tecnologias e Conceitos
* **FastAPI (Python 3.13)**: Backend assíncrono de alta performance.
* **Segurança JWT**: Autenticação OAuth2 com tokens JSON Web Token.
* **SQLAlchemy Async**: ORM moderno com suporte assíncrono.
* **Streamlit & Plotly**: Dashboard interativo com engenharia de atributos.
* **Docker**: Infraestrutura isolada e reprodutível.
* **Qualidade**: Testes de integração cobrindo fluxos de segurança e analytics.

## 📊 Dashboard de Business Intelligence
O dashboard integrado permite visualizar:
* **Métricas Gerais**: Ticket médio, volumetria e amplitude de preços.
* **Mix de Produtos**: Distribuição percentual por faixa de preço.
* **Análise de Valor**: Gráficos comparativos de preços por SKU.

## 🚀 Como Executar

### 1. Subir a Infraestrutura (Docker)
```bash
docker compose up --build -d
```
API disponível em: http://localhost:8000/docs

### 2. Popular o Banco (Seed)
Para gerar dados de teste e validar os gráficos:
```bash
poetry run python seed.py
```

### 3. Abrir o Dashboard (Streamlit)
```bash
poetry run streamlit run dashboard.py
```
Acesse: http://localhost:8501 (Credenciais geradas pelo seed: carlos / 123)

## 📚 Documentação da API

A referência funcional dos endpoints, autenticação, exemplos e códigos HTTP está em [`docs/API.md`](docs/API.md). A documentação interativa também fica disponível em `/docs` quando a API está em execução.

## 🧪 Qualidade de Código
Para rodar a suíte de testes localmente:
```bash
poetry run pytest --cov=products_api --cov-report=html
```

---
Desenvolvido por **Carlos Henrique Junior** - Integrando Engenharia de Software e Data Analytics.
