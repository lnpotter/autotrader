# Autotrader - Forked from Marcelo Ferraz de Oliveira

Este repositório contém um sistema automatizado de negociação para a corretora Clear, desenvolvido com Python e Selenium.

## Funcionalidades Principais

- **Login Automatizado**: Realiza o login na plataforma da Clear utilizando credenciais fornecidas via variáveis de ambiente.
- **Consulta de Saldo**: Obtém o saldo disponível na Clear, incluindo investimentos em Tesouro Direto.
- **Compra e Venda Automatizadas**: Monitora o livro de ofertas da ação escolhida pelo usuário e realiza operações de compra e venda baseadas em condições predefinidas.
- **Rebalanceamento Automático**: Calcula automaticamente a quantidade a ser comprada ou vendida para manter o equilíbrio da carteira.

## Requisitos

- Docker
- ChromeDriver
- Navegador Chromium
- Python 3.x

## Instalação e Execução com Docker

1. **Clonagem do Repositório**:
   - Clone este repositório: `git clone https://github.com/lnpotter/autotrader`
   - Entre no diretório do projeto: `cd autotrader`

2. **Construção e Execução com Docker**:
   - Construa a imagem Docker:
     ```
     docker build -t autotrader .
     ```
   - Execute o contêiner Docker:
     ```
     docker run --rm -it --name autotrader autotrader - AVISO! Mantenha-se na página do ativo que deseja comprar para a automação detectar os elementos de compra e venda e conseguir manipulá-los com sucesso!
     ```

## Configuração das Variáveis de Ambiente

Antes de executar o contêiner Docker, defina as seguintes variáveis de ambiente no seu sistema:

- `CPF`: CPF associado à conta na Clear.
- `DATA_NASCIMENTO`: Data de nascimento do usuário.
- `SENHA`: Senha de acesso à Clear.
- `ASSINATURA`: Assinatura eletrônica para confirmação de operações.
- `SALDO_EXTERNO`: Saldo externo disponível para investimentos.
- `STEP`: Passo inicial para otimização das operações de trading.

## Uso

Para utilizar o autotrader para negociar um ativo específico na Clear, siga os passos abaixo:

1. **Escolha do Ativo**:
   - Certifique-se de que está na página do ativo desejado na Clear.

2. **Configuração do Código**:
   - No arquivo `main.py`, ajuste os parâmetros de trading conforme necessário, como preço de compra, preço de venda, etc.

3. **Execução**:
   - Execute o contêiner Docker com as variáveis de ambiente configuradas para iniciar a negociação automatizada.

## Contribuições

- Este projeto é um fork do repositório original de [Marcelo Ferraz de Oliveira](https://github.com/Marcelo-Ferraz-de-Oliveira).
- Contribuições são bem-vindas através de pull requests.
