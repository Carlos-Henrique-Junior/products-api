# Products API

Documentação funcional da API de gerenciamento de produtos.

## Acesso local

- Base URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI: `http://localhost:8000/openapi.json`

## Autenticação

A autenticação usa OAuth2 Password Flow com token JWT.

### Criar usuário

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H 'Content-Type: application/json' \
  -d '{"username":"carlos","password":"senha-segura"}'
```

### Obter token

O endpoint recebe formulário URL-encoded, não JSON:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=carlos&password=senha-segura'
```

Resposta esperada:

```json
{"access_token":"<JWT>","token_type":"bearer"}
```

Use o token nas rotas protegidas:

```text
Authorization: Bearer <JWT>
```

## Endpoints

### GET `/health_check`

Verifica se a API está disponível.

Resposta `200`:

```json
{"status":"ok"}
```

### GET `/api/v1/products/`

Lista os produtos cadastrados. Pode ser acessado sem autenticação.

### POST `/api/v1/products/`

Cria um produto.

Corpo:

```json
{
  "name": "Teclado Mecânico RGB",
  "price": 350.90,
  "description": "Teclado switch blue com layout ABNT2"
}
```

Respostas comuns: `201` para criação e `422` para dados inválidos.

### PUT `/api/v1/products/{product_id}`

Substitui os dados do produto. Recebe o mesmo corpo do POST.

### PATCH `/api/v1/products/{product_id}`

Atualiza parcialmente um produto:

```json
{"price": 299.90}
```

### DELETE `/api/v1/products/{product_id}`

Remove o produto informado.

### GET `/api/v1/products/stats`

Retorna estatísticas agregadas dos produtos. Requer JWT.

Resposta esperada:

```json
{
  "total_count": 1,
  "average_price": "99.90",
  "min_price": "99.90",
  "max_price": "99.90"
}
```

## Status HTTP

- `200`: operação concluída.
- `201`: recurso criado.
- `401`: autenticação ausente ou inválida.
- `404`: recurso não encontrado.
- `422`: corpo ou parâmetros inválidos.
- `500`: erro interno; investigar logs do serviço.

## Execução

```bash
docker compose up --build -d
# ou
poetry install
poetry run uvicorn products_api.app:app --reload --port 8000
```

Testes automatizados:

```bash
poetry run pytest -q
```

## Segurança

Não publique `.env`, tokens ou credenciais. Em produção, use HTTPS, limite de requisições, headers de segurança, CORS restrito e uma chave JWT forte fora do código-fonte.
