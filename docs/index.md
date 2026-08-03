![logo do projeto](assets/logo-lunar.png){ width="300" .center }
# Bem vindo ao Lunar CLI

Lunar é um CLI para auxiliar no início da criação de projetos `python`, permitindo que você, através de uma linha de comando, crie a estrutura inicial de um projeto, utilizando poetry como gerenciador de dependências, entre outras funcionalidades.

# Instalação

É recomendado que você utilize o `pipx`, uma excelente ferramenta para instalação de pacotes globais.

```console
$ pipx install ln-cli
```

Veja o guia completo de [instalação](instalação.md) para outras formas de instalar (pip, clone do repositório, build local, etc).

# Como utilizar

Você pode chamar o lunar via linha de comando:

```console
$ lunar new api projeto

Projeto criado
```

Este comando vai criar um diretório novo com a estrutura mínima para iniciar a construção de um novo projeto.

Estão disponíveis três flags para adicionar pacotes ao projeto no momento da criação:

* `--fastapi` - instala fastapi e suas dependências.
* `--django` - instala django-ninja e suas dependências.
* `--dev` - instala as dependências de desenvolvimento (testes, lint, etc).

## Mais informações sobre o CLI e seus comandos

Você pode obter instruções utilizando a flag `--help`

```console
$ lunar --help

 Usage: lunar [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                                                                                                           │
│ --install-completion          Install completion for the current shell.                                             │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.      │
│ --help                        Show this message and exit.                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ new                                                                                                                 │
│ install                                                                                                             │
│ docker                                                                                                              │
│ linux-tips                                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

A flag `--help` também está disponível para cada comando do CLI

```console
$ lunar new api --help

Usage: lunar new api [OPTIONS] {name}

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    name      <str>  Cria um projeto [required]                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --fastapi          Instala dependências do FastAPI                                                                 │
│ --django           Instala dependências do Django                                                                  │
│ --dev              Instala dependências de desenvolvimento                                                         │
│ --help             Show this message and exit.                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
