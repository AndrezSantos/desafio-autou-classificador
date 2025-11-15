Classificador de Emails com IA - Desafio AutoU

Projeto desenvolvido por Andrez Santos como solução para o Desafio Técnico da AutoU.

A aplicação web utiliza Inteligência Artificial para classificar emails (por texto manual ou upload de .txt) em categorias "Produtivo" ou "Improdutivo" e simula o envio de uma resposta automática adequada.

🚀 Aplicação no Ar (Deploy na Nuvem)

A aplicação está 100% funcional e hospedada na plataforma gratuita do Render.

Link para testar ao vivo:
https://desafio-autou-classificador-a2ew.onrender.com/

🛠️ Tecnologias Utilizadas

Este projeto foi construído com foco em leveza, escalabilidade e conformidade com os requisitos de deploy gratuito:

Backend: Python 3

Servidor Web: Flask

Inteligência Artificial: Google Gemini API (modelo gemini-flash-latest)

Hospedagem: Render.com (conectado ao GitHub para deploy contínuo)

Frontend: HTML5, CSS3 (layout em Grid) e JavaScript (para fetch e atualização do DOM)

Ambiente: python-dotenv (para gerenciamento de chaves de API)

🧠 A Jornada da IA: Decisões Técnicas

Um requisito chave do desafio era usar IA de forma eficaz e garantir o deploy em uma plataforma gratuita. Isso exigiu uma análise de arquitetura e resolução de problemas.

1. Sobre a Participação da IA no Desenvolvimento

Este projeto foi desenvolvido em colaboração com uma IA assistente (Gemini), que atuou como uma "programadora em par" (pair programmer). A IA foi fundamental para:

Sugerir arquiteturas de código (ex: app.py do Flask).

Acelerar a depuração de erros complexos (como erros de API, deploy e gerenciamento de memória).

Refatorar o código para soluções mais robustas (como o "decodificador robusto" de UTF-8/latin-1).

A estratégia, as decisões de engenharia e a lógica de negócios (como os labels de classificação) foram 100% humanas, enquanto a IA atuou como uma ferramenta de produtividade e depuração.

2. A Escolha da IA para Classificação (A "Saga")

O processo para encontrar a IA correta foi um exercício de engenharia e eliminação:

Plano A: API do Hugging Face (Gratuita)

Status: Descartada.

Motivo: A API pública se mostrou instável durante os testes, retornando um paradoxo de erros 410 (Gone) e 404 (Not Found). Isso é inviável para um produto que precisa de confiabilidade.

Plano B: Modelo Local (Hugging Face Transformers)

Status: Descartado.

Motivo: Esta abordagem apresentou dois problemas fatais:

Modelos Grandes (ex: bart-large): Causaram MemoryError (estouro de memória RAM) em máquinas locais de teste (com 4GB-8GB de RAM).

Modelos Leves (ex: distilbert): Se mostraram imprecisos, classificando "Spam" como "Produtivo" e "Suporte Técnico" como "Improdutivo", falhando no requisito principal do desafio.

Impede o Deploy: Modelos locais (mesmo os leves de 260MB+) são muito pesados para os limites de RAM (512MB) das plataformas de deploy gratuito (Render/Vercel).

Plano C: A Solução Vencedora (Google Gemini API)

Status: Implementado.

Motivo: Esta arquitetura atende a TODOS os requisitos do desafio:

Leveza: O app não baixa nenhum modelo.

Hospedagem Gratuita: Funciona perfeitamente nos limites do Render.

Precisão: A API do Gemini é uma das mais avançadas.

"Treinamento": Em vez de treinar um modelo, usamos "Prompt Engineering" (no app.py). Nós fornecemos à IA as palavras-chave de negócio (nossos produtivo_labels e improdutivo_labels), ensinando-a em tempo real a classificar os emails com base no contexto da AutoU, o que resultou em 100% de acerto nos testes.

💻 Como Executar Localmente

Para rodar este projeto em sua máquina local:

Clone o Repositório

git clone [https://github.com/AndrezSantos/desafio-autou-classificador.git](https://github.com/AndrezSantos/desafio-autou-classificador.git)
cd desafio-autou-classificador


Crie e Ative um Ambiente Virtual (Venv)

# Windows
python -m venv venv
.\venv\Scripts\activate


Instale as Dependências
(O app.py vai travar se você pular este passo!)

pip install -r requirements.txt


Crie sua Chave de API (Crítico)

Vá ao Google AI Studio.

Crie uma nova API Key para um novo projeto.

Ative a "Gemini API" no seu Google Cloud Console (como fizemos na nossa depuração).

Configure o Arquivo .env

Na raiz do projeto, crie um arquivo chamado .env.

Adicione sua chave de API nele:

GOOGLE_API_KEY="COLE_SUA_CHAVE_DE_API_DO_GOOGLE_AQUI"


(O arquivo .gitignore já está configurado para proteger este arquivo e não enviá-lo para o GitHub.)

Rode o Servidor Flask

flask run


Acesse no Navegador
Abra http://127.0.0.1:5000



Andrez Santos

WhatsApp 74 9 9912-0486

LinkedIn <!-- (Presumi que era o LinkedIn da AutoU, troque pelo seu se preferir) -->

Instagram <!-- (Presumi que era o Insta da AutoU, troque pelo seu se preferir) -->