# MsEquipesTecnicas

Sistema de gerenciamento de equipes técnicas e seus membros, desenvolvido em Flask com SQLAlchemy e PostgreSQL.

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
├── app.py                # Arquivo principal da aplicação Flask
├── requirements.txt      # Dependências do projeto
├── models/               # Modelos ORM (Equipe, Membro, Enum)
├── routes/               # Rotas da API (equipe, membro)
└── rotas_documentadas.txt# Documentação das rotas
```

## Instalação
1. Crie e ative um ambiente virtual:
   ```
   python -m venv .venv
<<<<<<< HEAD
   ```
2. No Windows, ative o ambiente virtual:
   ```
=======
>>>>>>> aa39e6cc3ce45882062a878e176f643fdfed8fdd
   .venv\Scripts\activate
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Configure o banco PostgreSQL e ajuste a string de conexão em `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco'
   ```
4. Execute a aplicação:
   ```
   python app.py
   ```

## Exemplos de Requisições
### Criar uma Equipe
```json
{
  "nome": "Equipe Alpha",
  "especialidade": "Desenvolvimento",
  "status": "ativa"
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
- Para expor localmente via Cloudflare Tunnel:
- Instalação do Cloudflare Tunnel:

  ```
  winget install cloudflare.cloudflared
  ```
  ```
  cloudflared tunnel --url http://localhost:5000
  ```

## Autor Subruel
Projeto acadêmico para a disciplina de Sistemas Distribuídos.

