#!/bin/bash

# Roda as migrações do banco de dados
echo "Aplicando migrações do banco..."
python -m alembic upgrade head

# Inicia a aplicação
echo "Iniciando FastAPI..."
exec python -m uvicorn products_api.app:app --port 8000 --host 0.0.0.0
