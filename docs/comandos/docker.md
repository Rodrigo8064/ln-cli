# Docker

O comando `postgres` sobe um container Docker com um banco Postgres, pronto para ser usado em testes de API.

## Uso

```bash
lunar docker postgres [TAG] [NAME] [USER] [DB]
```

Todos os argumentos são posicionais e opcionais — se não forem informados, os valores padrão são usados.

## Argumentos

| Argumento | Descrição                          | Padrão          |
|-----------|--------------------------------------|-------------------|
| `TAG`     | Versão da imagem do Postgres        | `latest`          |
| `NAME`    | Nome do container                    | `app_database`    |
| `USER`    | Usuário do banco de dados           | `user`            |
| `DB`      | Nome do banco de dados               | `postgres_db`     |

!!! warning "Ordem importa"
    Como os argumentos são posicionais (não são flags como `--tag`), a ordem em que você os informa é sempre `TAG NAME USER DB`. Se quiser mudar só o `USER`, por exemplo, ainda assim precisa informar `TAG` e `NAME` antes dele.

## Exemplos

Subir o Postgres com todos os valores padrão:

```bash
lunar docker postgres
```

Subir uma versão específica do Postgres:

```bash
lunar docker postgres 17
```

Subir com nome de container, usuário e banco customizados (mantendo a tag `latest`):

```bash
lunar docker postgres latest meu_banco admin minha_api_db
```

## O que o comando cria

O container é criado com um volume fixo, além dos valores informados (ou padrão) para tag, nome, usuário, banco e porta:

| Configuração  | Valor                          |
|----------------|----------------------------------|
| Volume         | `pgdata:/var/lib/postgresql/`   |
| Senha          | `password`                      |

!!! warning "Senha fixa"
    A senha do banco continua fixa no código (`password`) — ainda não há argumento para customizá-la. Esse comando foi pensado para ambientes de desenvolvimento/teste local; não use essa senha em produção.

!!! note "Container já existente"
    Se já existir um container com o mesmo `NAME` (por exemplo, de uma execução anterior), o Docker vai recusar a criação com um erro de nome duplicado. Remova o container antigo (`docker rm -f NOME`) antes de rodar o comando de novo, ou use um `NAME` diferente para rodar vários bancos ao mesmo tempo.
