# Desafio - Classificador de Emails (AutoU)

Projeto: Desafio Autou 
Dev....: **Andrez Santos**.

Este projeto é uma aplicação web simples que utiliza IA (Hugging Face) para classificar emails como "produtivos" ou "improdutivos" e enviar uma resposta automática.

## Tecnologias Utilizadas

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Inteligência Artificial:** Hugging Face Transformers 
(modelo `MoritzBinary/portuguese-bert-cased-finetuned-portuguese-nli`)
- **Envio de Email:** `smtplib` (Python)

## Como Executar Localmente (Com VS Code)

1.  **Clone o Repositório**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd desafio_autou
    ```

2.  **Crie um Ambiente Virtual** (Boa prática para não misturar bibliotecas)
    ```bash
    python -m venv venv
    ```
    - No Windows: `.\venv\Scripts\activate`
    - No Mac/Linux: `source venv/bin/activate`

3.  **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: A biblioteca `torch` ou `tensorflow` pode ser grande e demorar um pouco.)*

4.  **Execute a Aplicação**
    ```bash
    flask run
    ```
    *O modelo de IA será baixado na primeira execução.*

5.  **Acesse no Navegador**
    Abra [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## [!] Atenção - Envio de Email [!]

A funcionalidade de envio de email automático (com `smtplib`) é sensível.

1.  **Use uma Conta de Teste:** Crie um novo email (ex: Gmail) apenas para este projeto.
2.  **Use "Senhas de App":** Se usar o Gmail, você precisa ativar a "Verificação em 2 Etapas" e depois gerar uma "Senha de App" (App Password). Você **NÃO** usará sua senha normal do Gmail.
3.  **Não suba sua senha** para o GitHub. Os campos no formulário são para teste local. Para produção/deploy, use Variáveis de Ambiente.