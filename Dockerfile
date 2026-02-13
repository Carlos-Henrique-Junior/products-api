FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends     curl     build-essential     && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Primeiro copiamos tudo para que o Poetry veja a estrutura do projeto
COPY . .

# Instalamos as dependências
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main

# Garante que o script de entrada tenha permissão
RUN chmod +x entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
