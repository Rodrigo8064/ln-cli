# Criando projetos

O comando `new api` cria a estrutura inicial de um projeto usando o [Poetry](https://python-poetry.org/) e, opcionalmente, já instala as dependências e os arquivos básicos de um framework web.

## Uso

```bash
lunar api NOME_DO_PROJETO [OPÇÕES]
```

Onde `NOME_DO_PROJETO` é o nome da pasta que será criada para o projeto.

## Opções

| Opção        | Descrição                                                      |
|--------------|------------------------------------------------------------------|
| `--fastapi`  | Instala as dependências do FastAPI e cria um `app.py` inicial. |
| `--django`   | Instala as dependências do Django.                              |
| `--dev`      | Instala as dependências de desenvolvimento (testes, lint, etc). |

!!! warning "Escolha apenas um framework"
    As flags `--fastapi` e `--django` são mutuamente exclusivas. Se as duas forem passadas juntas, o comando exibe um aviso e é encerrado sem criar nada.

A flag `--dev` pode ser combinada livremente com `--fastapi` ou `--django`.

## Exemplos

Criar um projeto vazio, sem nenhuma dependência extra:

```bash
lunar api meu-projeto
```

Criar um projeto FastAPI, já com o `app.py` inicial:

```bash
lunar api minha-api --fastapi
```

Criar um projeto Django com as dependências de desenvolvimento:

```bash
lunar api meu-app --django --dev
```

## O que acontece por trás dos panos

1. O comando roda `poetry new --flat NOME_DO_PROJETO`, criando a estrutura padrão do Poetry.
2. Se `--fastapi` for usado, os pacotes do grupo `fastapi` são instalados via [`install_packages`](#ln_cli.commands.install_packages) e um `app.py` com um endpoint `/health_check` é criado dentro do projeto.
3. Se `--django` for usado, os pacotes do grupo `django` são instalados.
4. Se `--dev` for usado, os pacotes do grupo `dev` são instalados via `install_packages_dev`.

Os pacotes instalados em cada caso vêm do dicionário `packages`:

```python
packages: dict[str, list[str]] = {
    'fastapi': [
        'fastapi[standard]',
        'sqlalchemy',
        'alembic',
        'psycopg[binary]',
    ],
    'django': ['django-ninja', 'psycopg[binary]'],
    'dev': ['pytest', 'taskipy', 'ruff', 'testcontainers', 'pytest-cov'],
}
```
