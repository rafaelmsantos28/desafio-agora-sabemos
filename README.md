
# Consulta Qualis CAPES - Desafio Técnico Agora Sabemos

Este projeto é um protótipo de ferramenta desenvolvida para auxiliar coordenadores de pós-graduação na consulta e análise das classificações de periódicos científicos do sistema QUALIS (CAPES).

A aplicação é composta por um pipeline de extração e carga de dados (ETL simples), uma API RESTful para servir as informações e uma interface interativa para visualização e filtragem.

## Tecnologias Usadas

* **Python 3.10+**: Linguagem base.
* **Pandas + SQLite3**: Utilizados para a engenharia de dados (leitura da planilha, limpeza e armazenamento no banco dados).
* **FastAPI**: Utilizado para o back-end (alta performance e documentação automática com Swagger).
* **Streamlit**: Utilizado para o front-end (visualização limpa e orientada a dados)

## Executando o projeto (Sem Docker)

Siga os passos abaixo para rodar a aplicação em sua máquina.

**1. Clone o repositório e acesse a pasta:**
```bash
git clone https://github.com/rafaelmsantos28/desafio-agora-sabemos.git
cd desafio-agora-sabemos
```

**2. Crie e ative um ambiente virtual (recomendado):**

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Construa o banco de dados (ETL):**

```bash
python database_builder.py
```

_(Este comando lerá o arquivo `.xlsx` e gerará o arquivo `qualis.db` na raiz do projeto)._

**5. Inicie a API (Backend):**

```bash
uvicorn main:app --reload
```

A API estará rodando em `http://127.0.0.1:8000`. Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

**6. Inicie a Interface (Frontend):** Abra um novo terminal (mantenha a API rodando) e execute:

```bash
streamlit run app.py
```

A interface abrirá automaticamente no seu navegador em `http://localhost:8501`.

### Executando com Docker (Recomendado)

Para garantir que a aplicação rode perfeitamente em qualquer ambiente sem necessidade de instalar as dependências manualmente, o projeto foi containerizado.

Certifique-se de ter o [Docker](https://www.docker.com/) e o Docker Compose instalados.

Na raiz do projeto, execute apenas um comando:
```bash
docker-compose up --build
```

O Docker construirá a imagem, executará o ETL (database_builder.py) automaticamente para gerar o banco de dados e subirá os dois serviços:

API (FastAPI): Disponível em http://localhost:8000/docs

Dashboard (Streamlit): Disponível em http://localhost:8501



## Decisões Técnicas

-   **ETL prévio em vez de leitura em tempo real:** O arquivo em Excel enviado para o desafio tinha mais de 8.000 linhas, então cada requisição geraria queda de performance. Optei por criar um script preparatório que estrutura os dados em um banco SQLite, criando índices para as colunas de busca. Isso garante velocidade na resposta da API.

- **Sanitização de Dados (URL-Safe):** Durante a etapa de ETL, identifiquei que a base original possuía caracteres especiais como `/` nos nomes das áreas de avaliação. Para manter um padrão RESTful da API sem causar conflitos de roteamento, o script realiza a limpeza e substituição desses caracteres.

-   **FastAPI para o Backend:** A escolha se deu pela agilidade no desenvolvimento e pela facilidade de criação de rotas que ela traz. A documentação Swagger gerada automaticamente também facilita os testes.

-   **Streamlit para o Frontend:** Considerei seu design limpo, minha experiência prévia com a ferramenta e o prazo estabelecido do desafio. Ele entrega uma interface funcional, com filtros intuitivos e gráfico de barras sem adicionar complexidade desnecessária de infraestrutura de front-end.
    

## O que eu faria diferente com mais tempo

Se houvesse mais tempo para expandir este projeto, minhas próximas ações seriam:

1.  **Evolução Arquitetural:** Separaria as responsabilidades de extração/carga e a API de consulta em uma arquitetura de microsserviços. Aplicaria princípios SOLID para garantir que as regras de negócio do domínio Qualis ficassem completamente isoladas da camada de infraestrutura e persistência.
    
2.  **Testes Automatizados:** Colocaria testes unitários e de integração utilizando a biblioteca `pytest` para cobrir os principais cenários dos endpoints.
    
3.  **Banco de Dados Robusto:** Migraria do SQLite para um banco PostgreSQL hospedado na nuvem, facilitando a concorrência de acessos.