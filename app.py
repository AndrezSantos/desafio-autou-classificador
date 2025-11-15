# --- Importações de Bibliotecas ---
from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json # Para processar a resposta da API
import re # Para extrair o JSON da resposta de texto

# --- Configuração da API do Gemini ---
load_dotenv()


# --- Labels Inteligentes (para o Prompt) ---
produtivo_labels = "solicitação, suporte, técnico, dúvida, sistema, atualização, erro, treinamento, implantação, software, problema, hardware, impressora, módulo"
improdutivo_labels = "precisando, hobby, relacionamento, conhecer, conheça, loja, interesse, produto, compra, promoção, cupom, chat, propaganda, spam, newsletter, agradecimento, felicitação, marketing"

# --- Configuração Inicial ---
app = Flask(__name__)

# --- Função Auxiliar: Classificação com GEMINI API ---
def classify_text_gemini_api(text_to_classify):
    """
    Classifica o texto usando a API do Google Gemini (modelo gemini-pro).
    """
    
    # --- CORREÇÃO 502 ---
    # a configuração da API para DENTRO da função.
    # O app só vai tentar configurar a API quando esta função for chamada.
    GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GEMINI_API_KEY:
        raise Exception("API Key do Google não configurada no ambiente do Render.")
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("API do Google Gemini configurada (on-demand).")
    except Exception as e:
        print(f"Erro ao configurar a API do Gemini: {e}")
        raise Exception(f"Erro ao configurar a API do Gemini: {e}")
    # --- FIM DA CORREÇÃO ---
        
    print("Enviando texto para a API do Google Gemini (models/gemini-flash-latest)...")
    
    try:
        model = genai.GenerativeModel(model_name="models/gemini-flash-latest")

        #implementando esse codigo para debugar os modelos disponíveis
        models = genai.list_models()
        for m in models:
            print(m.name, m.supported_generation_methods)




        prompt = f"""
        Você é um classificador JSON.
        Analise o e-mail abaixo e classifique-o como 'produtivo' ou 'improdutivo' com base nas seguintes palavras-chave:

        - 'produtivo': {produtivo_labels}
        - 'improdutivo': {improdutivo_labels}

        Responda APENAS com o objeto JSON. Não inclua "json", "```", ou qualquer outro texto.
        O formato da sua resposta deve ser:
        {{"categoria": "...", "confianca": 0.0}}

        E-mail para analisar:
        ---
        {text_to_classify}
        ---
        """
        
        response = model.generate_content(prompt)
        
        print(f"Resposta bruta da API: {response.text}")
        
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if not match:
            raise Exception("A API do Gemini não retornou um JSON válido.")
            
        json_text = match.group(0)
        result_json = json.loads(json_text)
        
        return {
            'labels': [result_json.get('categoria', 'erro')],
            'scores': [result_json.get('confianca', 0.0)]
        }
        
    except Exception as e:
        print(f"ERRO NA API DO GEMINI: {e}")
        raise Exception(f"Erro ao contatar a API do Gemini: {e}")


# --- Rotas da Aplicação ---

@app.route('/')
def home():
    """ Rota principal que carrega o 'index.html' """
    return render_template('index.html')


@app.route('/classificar', methods=['POST'])
def classificar_email():
    """ Rota que recebe o formulário (texto ou .txt) e classifica """
    
    try:
        # --- 1. Obter Dados do Formulário ---
        dados = request.form
        arquivo = request.files.get('arquivoEmail')
        texto_email = ""

        # --- 2. Lógica de Leitura (Upload ou Texto) ---
        if arquivo and arquivo.filename != '':
            if not arquivo.filename.lower().endswith('.txt'):
                raise ValueError("Arquivo inválido. Por favor, envie apenas .txt.")
            
            bytes_brutos = arquivo.stream.read()
            texto_bruto = ""
            
            try:
                print("Tentando decodificar arquivo como UTF-8...")
                texto_bruto = bytes_brutos.decode("utf-8")
                print("Decodificado com UTF-8.")
            except UnicodeDecodeError:
                print("Falha no UTF-8. Tentando decodificar como Latin-1...")
                texto_bruto = bytes_brutos.decode("latin-1")
                print("Decodificado com Latin-1.")

            
            linhas = texto_bruto.splitlines()
            inicio_corpo = 0
            
            for i, linha in enumerate(linhas):
                if linha.lower().startswith("assunto:"):
                    inicio_corpo = i + 1 
                    break
            
            if inicio_corpo > 0:
                print("Arquivo .txt detectado. Removendo cabeçalhos (antes de 'Assunto:')...")
                texto_email = "\n".join(linhas[inicio_corpo:])
            else:
                print("Arquivo .txt não parece ter cabeçalho 'Assunto:'. Usando texto completo.")
                texto_email = texto_bruto
                
        elif dados.get('corpoEmail'):
            print("Texto manual detectado.")
            texto_email = dados.get('corpoEmail')
        else:
            raise ValueError("Nenhum texto ou arquivo .txt foi enviado.")
        
        if len(texto_email.strip()) < 10:
             raise ValueError("Texto muito curto (após limpeza). Escreva um email mais completo.")

        # --- 3. Coletar Outros Dados do Formulário ---
        nome_fantasia = dados.get('nomeFantasia')
        email_remetente_app = dados.get('emailResposta')
        senha_email_remTente = dados.get('senhaEmail') 
        email_destinatario = dados.get('emailOriginal')
        resposta_produtiva = dados.get('respostaProdutiva')
        resposta_improdutiva = dados.get('respostaImprodutiva')

        if not senha_email_remTente:
            raise ValueError("A 'Sua Senha (Simulada)' não pode estar vazia.")

        # --- 4. LÓGICA DE CLASSIFICAÇÃO (API GEMINI-PRO) ---
        resultado = classify_text_gemini_api(texto_email)
        print(f"Resultado da API Gemini recebido: {resultado}")
        
        categoria = resultado['labels'][0]
        confianca = resultado['scores'][0]

        # --- 5. Lógica de Resposta Automática ---
        resposta_sugerida = ""
        if categoria == 'produtivo':
            resposta_sugerida = resposta_produtiva
        else:
            resposta_sugerida = resposta_improdutiva

        # --- 6. Enviar o Email (Simulado) ---
        enviar_email_resposta(
            nome_fantasia,
            email_remetente_app,
            senha_email_remTente, 
            email_destinatario,
            resposta_sugerida
        )
        status_envio = "Email de resposta automática (simulado) enviado com sucesso."

        # --- 7. Enviar Resultado de Volta (JSON) ---
        return jsonify({
            'categoria': categoria,
            'confianca': f"{(confianca * 100):.2f}%",
            'resposta_sugerida': resposta_sugerida,
            'status_envio': status_envio
        })

    except Exception as e:
        print(f"ERRO GERAL: {e}")
        return jsonify({'erro': str(e)}), 400

# --- Função Auxiliar: Envio de Email (SIMULADA) ---
def enviar_email_resposta(nome_fantasia, email_remetente, senha_remetente, email_destinatário, corpo_resposta):
    
    if not all([nome_fantasia, email_remetente, senha_remetente, email_destinatário, corpo_resposta]):
        raise ValueError("Dados insuficientes para simulação (Nome, Emails, Senha ou Corpo).")

    print("\n--- SIMULAÇÃO DE ENVIO DE EMAIL ---")
    print(f"De: {nome_fantasia} <{email_remetente}>")
    print(f"Para: {email_destinatário}")
    print(f"Assunto: Res: não responda a este email automático.")
    print(f"Corpo: {corpo_resposta}")
    print("--- FIM DA SIMULAÇÃO (Email não foi enviado de verdade) ---\n")
    

# --- Ponto de Partida ---
if __name__ == '__main__':
    # Adicionamos 're' à lista de importações
    import re
    app.run(debug=True, port=5000)

#Rota que ajudou a saber o mdelo ideal para a chave goggle gemini
#@app.route('/modelos')
#def listar_modelos():
#    """ Rota para listar os modelos disponíveis e seus métodos """
#    try:
#        modelos = genai.list_models()
#        lista = []
#       for m in modelos:
#            lista.append({
#               'nome': m.name,
#                'metodos_suportados': m.supported_generation_methods
#           })
#        return jsonify(lista)
#    except Exception as e:
#       return jsonify({'erro': str(e)}), 500