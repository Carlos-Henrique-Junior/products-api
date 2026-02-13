#!/bin/bash

# Roda as migrações do banco de dados
echo "Aplicando migrações do banco..."
poetry run alembic upgrade head

# Inicia a aplicação
echo "Iniciando FastAPI..."
exec fastapi run products_api/app.py --port 8000 --host 0.0.0.0
