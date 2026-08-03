# Instalação
 
É recomendado que você utilize o `pipx`, uma excelente ferramenta para instalação de pacotes globais.
 
```console
$ pipx install ln-cli
```
 
Você também pode utilizar um gerenciador da sua preferência como pip, poetry ou uv
 
```console
$ pip install ln-cli
```
 
Você também pode fazer um clone do projeto para sua máquina
 
```console
$ git clone https://github.com/Rodrigo8064/ln-cli.git
```
 
Instalar os pacotes com o gerenciador de dependências de sua preferência.
 
```console
$ poetry install
```
 
E testar com seu ambiente virtual ativo chamando o programa por seu nome
 
```console
$ lunar new --help
```
 
!!! tip
    Se você já tem uma maneira preferida de criar seus pacotes, pode pular esta parte.
 
## Criando o pacote
 
Para utilizar o lunar no ambiente global de sua máquina, faça o build do pacote com seu gerenciador de dependências
 
```console
$ poetry build
```
