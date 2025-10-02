# MsEquipesTecnicas

Sistema de gestão de equipes técnicas e os seus membros, desenvolvido em Flask com SQLAlchemy e PostgreSQL.

## Funcionalidades
- Cadastro, consulta, atualização e remoção de equipes técnicas
- Cadastro, consulta, atualização e remoção de membros de equipes
- Associação de membros às equipes

## Tecnologias Utilizadas
- Python 3.11+
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- psycopg2

## Estrutura de Pastas
```
MsEquipesTecnicas/
├── app.py                 # Arquivo principal da aplicação Flask
├── requirements.txt       # Dependências do projeto
├── models/                # Modelos ORM (Equipe, Membro, Enum)
├── routes/                # Rotas da API (equipe, membro)
├── rotas_documentadas.txt # Documentação das rotas
├── config.py              # Configurações da aplicação
└── README.md              # Documentação do projeto
```

## Instalação
1. Crie e ative um ambiente virtual:
   ```
   python -m venv .venv
   ```
2. No Windows, ative o ambiente virtual:
   ```
   .venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure o banco PostgreSQL, rotas de autenticação e microserviços. Ajuste a string(url) de conexão em `config.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco'
   ```
5. Execute a aplicação:
   ```
   python app.py
   ```

## Exemplos de Requisições

## Rotas da API

Prefixo: `/api/v1/`
### Endpoints
#### Equipes
- **GET** `/api/v1/equipes` - Lista todas as equipes.
- **GET** `/api/v1/equipes/<int:id>` - Obtém uma equipe pelo ID.
- **GET** `/api/v1/equipes?status=<string:status>` - Lista equipes por status (ativa/inativa).
- **GET** `/api/v1/equipes?especialidade=<string:especialidade>` - Lista equipes por especialidade.
- **GET** `/api/v1/equipes/status/ativa/<int:id>` - Retorna a equipe caso esteja ativa.
- **GET** `/api/v1/equipes/<int:id>/status` - Retorna o status da equipe.
- **POST** `/api/v1/equipes/` - Cria uma nova equipe.
- **PUT** `/api/v1/equipes/<int:id>` - Atualiza uma equipe existente.
- **PATCH** `/api/v1/equipes/<int:id>/<string:status>` - Atualiza o status da equipe.
- **DELETE** `/api/v1/equipes/<int:id>` - Remove uma equipe.

#### Membros
- **GET** `/api/v1/membros` - Lista todos os membros.
- **GET** `/api/v1/membros/<int:id>` - Obtém um membro pelo ID.
- **POST** `/api/v1/membros/` - Cria um novo membro.
- **PUT** `/api/v1/membros/<int:id>` - Atualiza um membro existente.
- **DELETE** `/api/v1/membros/<int:id>` - Remove um membro.



### Criar uma Equipe
```json
{
  "nome": "Equipe Alpha",
  "especialidade": "Desenvolvimento",
  "status": "ativa",
  // por padrão, o status é "ativa" caso não seja informado.
  "membros": [
    {
      "nome": "João Silva",
      "cargo": "Técnico",
      "contato": "joao@email.com"
    },
    {
      "nome": "Maria Souza",
      "cargo": "Engenheira",
      "contato": "maria@email.com"
    }
  ]
  // o campo "membros" é opcional e a quantidade é limitada a 10 membros.
}
```

### Criar um Membro

```json
{
  "nome": "João da Silva",
  "cargo": "Desenvolvedor",
  "contato": "joao@email.com",
  "equipe_id": 1
}
```

## Observações
- O campo `status` da equipe deve ser "ativa" ou "inativa".
- IDs das equipes e membros são autoincrementados pelo banco.

- Instalação do Cloudflare Tunnel:
  ```
  winget install cloudflare.cloudflared
  ```
- Para expor localmente via Cloudflare Tunnel:  
  ```
  cloudflared tunnel --url http://localhost:5000
  ```

## Autor Subruel
Projeto acadêmico para a disciplina de Sistemas Distribuídos.

