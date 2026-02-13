# 📦 Products Management API (Modern FastAPI) & BI Dashboard

![CI Status](https://github.com/Carlos-Henrique-Junior/products-api/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Standard-009688)
![Coverage](https://img.shields.io/badge/coverage-78%25-green)

Sistema completo de gerenciamento de inventário com foco em **segurança**, **performance** e **análise de dados**. O projeto une um backend robusto a um dashboard interativo para insights em tempo real.

## 🛠 Tecnologias e Conceitos
* **FastAPI (Python 3.13)**: Backend assíncrono de alta performance.
* **Segurança JWT**: Autenticação OAuth2 com tokens JSON Web Token.
* **SQLAlchemy Async**: Operações em banco de dados SQLite sem bloqueio.
* **Streamlit & Plotly**: Visualização de dados dinâmica com engenharia de atributos.
* **Docker**: Ambiente totalmente isolado e reprodutível.
* **Qualidade**: Testes de integração cobrindo fluxos de segurança e analytics.

## 📊 Dashboard de Business Intelligence
O dashboard integrado permite visualizar:
* **Métricas Gerais**: Ticket médio, volumetria e amplitude de preços.
* **Mix de Produtos**: Distribuição percentual por faixa de preço (Econômico, Intermediário, Premium).
* **Análise de Valor**: Gráficos comparativos de preços por SKU.

## 🚀 Como Executar

### 1. Subir a Infraestrutura (Docker)
```bash
docker compose up --build -d
```
API disponível em: http://localhost:8000/docs

### 2. Popular o Banco (Seed)
Para ver os gráficos com dados reais de exemplo, rode:
```bash
poetry run python seed.py
```

### 3. Abrir o Dashboard (Streamlit)
```bash
poetry run streamlit run dashboard.py
```
Acesse: http://localhost:8501 (Login padrão no seed: carlos / 123)

## 🧪 Qualidade de Código
Para rodar a suíte completa de testes e gerar o relatório de cobertura:
```bash
poetry run pytest --cov=products_api --cov-report=html
```

---
Desenvolvido por **Carlos Henrique Junior** - Integrando Engenharia de Software e Data Analytics.
