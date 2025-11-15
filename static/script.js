// 'DOMContentLoaded' espera o HTML ser totalmente carregado
document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. LÓGICA DAS ABAS (Atualizada para Sidebar) ---

    // Pega todos os botões da barra lateral
    const sidebarButtons = document.querySelectorAll('.sidebar-btn');
    
    // Pega todos os painéis de conteúdo (as seções #manual e #upload)
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Loop que passa por cada botão da sidebar
    sidebarButtons.forEach(button => {
        // Adiciona um "ouvinte" de clique
        button.addEventListener('click', function() {
            
            // Pega o alvo do botão (ex: 'manual-section')
            const targetTab = button.dataset.tab;

            // --- Remove 'active' de todos os botões e painéis ---
            sidebarButtons.forEach(btn => {
                btn.classList.remove('active');
            });
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
            });

            // --- Adiciona 'active' apenas no botão clicado e no painel alvo ---
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // --- 2. LÓGICA DO FORMULÁRIO (Quase idêntica) ---
    
    // Pegar referências dos elementos do HTML
    const form = document.getElementById('form-classificador');
    const resultadoContainer = document.getElementById('resultado-container');
    
    // Botão de envio
    const btnEnviar = document.getElementById('btn-enviar');
    const btnTexto = document.getElementById('btn-texto');
    const btnLoading = document.getElementById('btn-loading');

    // Elementos do Dashboard
    const spanTotal = document.getElementById('total-avaliado');
    const spanProdutivo = document.getElementById('total-produtivo');
    const spanImprodutivo = document.getElementById('total-improdutivo');

    // --- 3. Contadores do Dashboard ---
    let total = 0;
    let produtivos = 0;
    let improdutivos = 0;

    // --- 4. Lógica Principal: Envio do Formulário ---
    
    form.addEventListener('submit', function(evento) {
        
        // Impede que o formulário recarregue a página
        evento.preventDefault(); 
        
        // Coleta TODOS os dados do formulário
        const formData = new FormData(form);

        // --- Mostrar "Loading" ---
        btnTexto.style.display = 'none';
        btnLoading.style.display = 'inline';
        btnEnviar.disabled = true;
        resultadoContainer.innerHTML = '<p>Analisando...</p>';

        // --- Enviar os dados para o Backend (app.py) ---
        fetch('/classificar', {
            method: 'POST',
            body: formData  // Envia os dados (texto ou arquivo)
        })
        .then(response => {
            // Se a resposta não for OK, lemos o erro
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.erro || 'Erro desconhecido.');
                });
            }
            // Se foi OK, lemos a resposta JSON
            return response.json();
        })
        .then(dados => {
            // --- Sucesso! Recebemos os dados do app.py ---
            
            // Atualiza o dashboard
            atualizarDashboard(dados.categoria);

            // Mostra o resultado na tela
            // Usamos 'textContent' para evitar problemas de segurança (HTML Injection)
            resultadoContainer.innerHTML = ''; // Limpa o "Aguardando..."
            
            const pCategoria = document.createElement('p');
            pCategoria.innerHTML = `<strong>Categoria:</strong> ${dados.categoria} (${dados.confianca})`;
            
            const pResposta = document.createElement('p');
            pResposta.innerHTML = `<strong>Resposta Sugerida:</strong> ${dados.resposta_sugerida}`;

            const pStatus = document.createElement('p');
            pStatus.innerHTML = `<strong>Status do Envio:</strong> ${dados.status_envio}`;
            
            resultadoContainer.appendChild(pCategoria);
            resultadoContainer.appendChild(pResposta);
            resultadoContainer.appendChild(pStatus);
        })
        .catch(erro => {
            // --- Falha! Algo deu errado ---
            console.error('Erro no fetch:', erro);
            // Mostra o erro de forma amigável na tela
            resultadoContainer.innerHTML = `<p style="color: red;"><strong>Erro:</strong> ${erro.message}</p>`;
        })
        .finally(() => {
            // --- Limpeza (sempre executa) ---
            
            // Restaura o botão
            btnTexto.style.display = 'inline';
            btnLoading.style.display = 'none';
            btnEnviar.disabled = false;

            // Limpa o campo de upload de arquivo (se houver)
            // Isso permite enviar o mesmo arquivo de novo, se o usuário quiser
            const inputFile = document.getElementById('arquivoEmail');
            if(inputFile) {
                inputFile.value = '';
            }
        });
    });

    // --- 5. Função Auxiliar: Atualizar o Dashboard ---
    function atualizarDashboard(categoria) {
        total++;
        if (categoria === 'produtivo') {
            produtivos++;
        } else {
            improdutivos++;
        }
        spanTotal.textContent = total;
        spanProdutivo.textContent = produtivos;
        spanImprodutivo.textContent = improdutivos;
    }
});