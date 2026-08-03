# Comandos Linux

O comando `linux-tips commands` mostra uma tabela com comandos úteis do terminal Linux, organizados por categoria.

## Uso

```bash
lunar commands TIPO
```

Onde `TIPO` é uma das categorias listadas abaixo.

## Tipos disponíveis

| Tipo                 | Descrição                          |
|-----------------------|--------------------------------------|
| `texto`               | Processamento de texto              |
| `arquivos`             | Visualização de arquivos            |
| `diretorios`           | Arquivos e diretórios               |
| `permissoes`           | Permissões e propriedades           |
| `processos`            | Processos e desempenho              |
| `rede`                 | Rede                                |
| `compactar`            | Compactação e arquivamento          |
| `sistema`               | Usuário e sistema                   |
| `redirecionamento`     | Redirecionamento e pipes            |

## Exemplos

Ver comandos de processamento de texto:

```bash
lunar commands texto
```

Ver comandos de rede:

```bash
lunar commands rede
```

O resultado é exibido em uma tabela com duas colunas, nome do comando e descrição:

```bash
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Nome    ┃ Descrição                                   ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ grep    │ pesquisa por termos dentro de arquivos      │
│ sed     │ edita texto em fluxo (substituições, ...)   │
│ ...     │ ...                                         │
└─────────┴─────────────────────────────────────────────┘
```

## Erros

Se você passar um tipo que não existe, o comando lança um erro listando as opções válidas:

```bash
lunar commands invalido
```

```
KeyError: Esse tipo de comando não existe, tente os comando desta lista ['texto', 'arquivos', 'diretorios', 'permissoes', 'processos', 'rede', 'compactar', 'sistema', 'redirecionamento']
```

!!! note "Maiúsculas e minúsculas"
    O tipo digitado é convertido para minúsculo antes da busca, então `lunar commands TEXTO` funciona normalmente.
