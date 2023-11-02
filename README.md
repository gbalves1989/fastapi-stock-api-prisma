# fastapi-stock-api
Api desenvolvida em python usando framework FastAPI
## Framework e libs
- FastApi
- Prisma Client Python -> https://prisma-client-py.readthedocs.io/en/stable/
- PostgresSQL
- Api Documentada
- Autenticação JWT Bearer
- CORS
- Rate Limit -> lib slowapi
- Upload de images
- Prometheus e Grafana para observabilidade

## Testando a aplicação
- criar ambiente de dev
  - python -m venv venv
  - cd venv/Scripts
  - ./activate
- instalar as libs
  - pip install -r requirements.txt
- executar o comando para rodar o prisma migrate
  - prisma db push

- lembrar de colocar o ip da sua maquina em API_HOST

<img width="381" alt="json" src="https://github.com/gbalves1989/fastapi-stock-api/assets/44848446/4a705a39-3830-4c5e-bb2d-4b73abdc96be">

- executar a aplicação
  - python main.py
- para acessar a documentação
  - http://{seu-ip}:8000/docs

## Configurando prometheus e grafana
- acessar a pasta docker e configurar o ip da sua maquina abaixo:
- a porta da job app tem que igual o do arquivo .env configurado:
  
<img width="452" alt="prometheus" src="https://github.com/gbalves1989/fastapi-stock-api/assets/44848446/56da87ad-17a0-49d5-afcc-1d78aebfbc3c">

- subir os containers
  - docker-compose up -d
- acessar o grafana em http://localhost:3000
  - user -> admin
  - password -> pass@123
- criar uma configuração com prometheus
- e adicionar o dashboard conforme arquivo abaixo:
  
<img width="381" alt="json" src="https://github.com/gbalves1989/fastapi-stock-api/assets/44848446/1d6b317c-a4d1-4be5-ba2c-635960759c38">

## Segue abaixo como se comportará a aplicação:

<img width="627" alt="swagger" src="https://github.com/gbalves1989/fastapi-stock-api/assets/44848446/4d8aea9f-eaa0-457b-b8db-c824722d7998">

<img width="639" alt="grafana" src="https://github.com/gbalves1989/fastapi-stock-api/assets/44848446/bbe2a3b2-1d6c-41a1-87f7-8fe75e1c83cf">



