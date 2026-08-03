# Instalador de pacotes

Esse grupo de comandos instala ferramentas usadas no dia a dia de desenvolvimento (`pipx`, `poetry`, `lazygit`, `lazydocker`, `ripgrep`), detectando automaticamente o gerenciador de pacotes do seu sistema (`apt`, `dnf` ou `pacman`).

Se nenhum desses gerenciadores for encontrado, os comandos que dependem dele são interrompidos com uma mensagem de erro.

## `pipx`

Instala o [pipx](https://pypa.github.io/pipx/) via gerenciador de pacotes (em sistemas `apt`/`dnf`) ou via `pip` (nos demais casos).

```bash
lunar install pipx
```

- Se o `pipx` já estiver instalado, o comando avisa e encerra sem fazer nada.
- Pede confirmação antes de instalar.

## `poetry`

Instala o [Poetry](https://python-poetry.org/), com escolha interativa do método de instalação.

```bash
lunar install poetry
```

Ao rodar, você escolhe entre duas opções:

```
Como deseja instalar o poetry?
  [1] Via pipx
  [2] Via instalador oficial
```

- **Opção 1 (via pipx):** instala o `pipx` primeiro, caso ainda não esteja disponível, depois instala o Poetry e o plugin `poetry-plugin-shell` com `pipx inject`.
- **Opção 2 (via instalador oficial):** garante que o `curl` está disponível e executa o script oficial de instalação (`install.python-poetry.org`), depois adiciona o plugin `poetry-plugin-shell` com `poetry self add`.

Se o Poetry já estiver instalado, o comando avisa e encerra sem fazer nada.

## `lazygit`

Instala o [lazygit](https://github.com/jesseduffield/lazygit) via gerenciador de pacotes.

```bash
lunar install lazygit
```

!!! note "Repositório extra no Fedora/dnf"
    Em sistemas `dnf`, o comando habilita o repositório COPR `dejan/lazygit` antes de instalar, já que o lazygit não está nos repositórios padrão do Fedora.

## `lazydocker`

Instala o [lazydocker](https://github.com/jesseduffield/lazydocker) diretamente via script oficial (não usa o gerenciador de pacotes do sistema).

```bash
lunar install lazydocker
```

Requer que o `curl` já esteja instalado no sistema — se não estiver, o comando é interrompido com um erro.

## `ripgrep`

Instala o [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`) via gerenciador de pacotes.

```bash
lunar install ripgrep
```

## Comportamento em caso de erro

Todos os comandos seguem o mesmo padrão: se a instalação falhar (pacote não encontrado, comando indisponível, erro do subprocesso), uma mensagem de erro é exibida em vermelho no terminal e o comando encerra com código de saída `1`.

Se o comando já detectar que a ferramenta está instalada, ele avisa e encerra com código de saída `0`, sem tentar reinstalar.
