"""
Helper para o projeto com funções que podem ser utilizadas nos comandos.

Attributes:
    packages: Um dicionario com pacotes padrões para instalação nos projetos.
    INSTALL_COMMANDS: Um dicionario com comandos para instalação de pacotes via gerenciador de pacotes.
    COMMANDS_TYPES: Um dicionario com clis e suas definições de uso para linux.

Como importar para o projeto:

```Python
from ln_cli.commands import INSTALL_COMMANDS

>>> INSTALL_COMMANDS
{'apt': lambda pkg: ['sudo', 'apt', 'install', pkg], 'dnf': lambda pkg: ['sudo', 'dnf', 'install', pkg], 'pacman': lambda pkg: ['sudo', 'pacman', '-S', pkg],}
```
"""

import shutil
import subprocess
from collections.abc import Callable

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


def install_packages(packages: list[str], name: str) -> None:
    """
    Instala pacotes via poetry.

    Parameters:
        packages: Pacotes que serão instalados.
        name: Nome da pasta onde está o projeto.

    Returns:
        A função adiciona os pacotes ao projeto e nao retorna None.

    Examples:
        >>> install_packages(['fastapi', 'sqlalchemy'], 'nova_api')
    """
    subprocess.run(['poetry', 'add', *packages], cwd=name)


def install_packages_dev(packages: list[str], name: str) -> None:
    """
    Instala pacotes de desenvolvimento via poetry.

    Parameters:
        packages: Pacotes que serão instalados.
        name: Nome da pasta onde está o projeto.

    Returns:
        A função adiciona os pacotes ao projeto e nao retorna None.

    Examples:
        >>> install_packages_dev(['ruff', 'taskipy'], 'nova_api')
    """
    subprocess.run(['poetry', 'add', '--group', 'dev', *packages], cwd=name)


def get_package_manager() -> None | str:
    """
    Verifica qual gerenciador de pacotes está instalado no sistema.

    Returns:
        A função retorna uma string com o nome do gerenciador ou None

    Examples:
        >>> get_package_manager()
        'dnf'

    !!!Nota
        Cada sistema vai retornar um valor está função
    """
    if shutil.which('apt'):
        return 'apt'
    if shutil.which('dnf'):
        return 'dnf'
    if shutil.which('pacman'):
        return 'pacman'
    return None


INSTALL_COMMANDS: dict[str, Callable[[str], list[str]]] = {
    'apt': lambda pkg: ['sudo', 'apt', 'install', pkg],
    'dnf': lambda pkg: ['sudo', 'dnf', 'install', pkg],
    'pacman': lambda pkg: ['sudo', 'pacman', '-S', pkg],
}

COMMANDS_TYPES: dict[str, dict[str, str]] = {
    'texto': {
        'grep': 'pesquisa por termos dentro de arquivos',
        'sed': 'edita texto em fluxo (substituições, remoções, ...)',
        'awk': 'processa e manipula texto em colunas/campos',
        'cut': 'extrai colunas ou campos de uma linha',
        'sort': 'ordena linhas de um arquivo',
        'uniq': 'remove ou conta linhas duplicadas',
        'wc': 'conta linhas, palavras e caracteres',
        'tr': 'traduz ou remove caracteres',
        'cat': 'mostra o conteúdo completo de um arquivo',
        'head': 'mostra as primeiras linhas de um arquivo',
        'tail': 'mostra as últimas linhas',
        'less': 'visualiza arquivos grandes com paginação',
    },
    'arquivos': {
        'find': 'localiza arquivos/diretórios por nome, tipo, data, ...',
        'locate': 'busca rápida de arquivos usando um índice pré-construído',
        'ls': 'lista arquivos e diretórios',
        'cp': 'copia arquivos/diretórios',
        'mv': 'move ou renomeia arquivos',
        'rm': 'remove arquivos/diretórios',
        'touch': 'cria arquivo vazio ou atualiza data de modificação',
    },
    'diretorios': {
        'mkdir': 'cria diretórios',
        'rmdir': 'remove diretórios vazios',
        'cd': 'muda o diretório atual',
        'pwd': 'mostra o diretório atual',
        'tree': 'exibe estrutura de diretórios em árvore',
    },
    'permissoes': {
        'chmod': 'altera permissões de arquivos',
        'chown': 'altera dono/grupo de um arquivo',
        'umask': 'define permissões padrão para novos arquivos',
        'whoami': 'mostra o usuário atual',
        'su': 'troca de usuário',
        'sudo': 'executa comandos com privilégios de administrador',
    },
    'processos': {
        'top': 'mostra processos em execução e uso de recursos em tempo real',
        'htop': 'versão interativa e melhorada do top',
        'ps': 'lista processos em execução',
        'kill': 'encerra processos pelo PID',
        'killall': 'encerra processos pelo nome',
        'nice': 'inicia processo com prioridade ajustada',
        'renice': 'ajusta prioridade de processo já em execução',
        'jobs': 'lista processos em segundo plano da sessão atual',
    },
    'rede': {
        'ping': 'testa conectividade com um host',
        'curl': 'faz requisições HTTP/transferência de dados',
        'wget': 'baixa arquivos da internet',
        'ssh': 'conecta a máquinas remotas com segurança',
        'scp': 'copia arquivos entre máquinas via SSH',
        'netstat': 'mostra conexões de rede ativas',
        'ss': 'versão moderna do netstat',
        'traceroute': 'mostra o caminho de pacotes até um destino',
    },
    'compactar': {
        'tar': 'agrupa (e opcionalmente compacta) arquivos',
        'gzip': 'compacta arquivos no formato .gz',
        'gunzip': 'descompacta arquivos .gz',
        'zip': 'compacta arquivos no formato .zip',
        'unzip': 'descompacta arquivos .zip',
    },
    'sistema': {
        'free': 'mostra uso de memória RAM',
        'df': 'mostra uso de espaço em disco',
        'du': 'mostra tamanho de arquivos/diretórios',
        'uptime': 'mostra há quanto tempo o sistema está ligado',
        'uname': 'mostra informações do sistema/kernel (uname -a para detalhes)',
    },
    'redirecionamento': {
        '|': 'Encadeira comandos',
        '>/>>': 'Redireciona saída para um arquivo',
        '&&': 'Executa o próximo comando somente se o anterior tiver sucesso',
    },
}
