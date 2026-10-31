const LivrariaClientController = {
    async inicializar() {
        try {
            await Promise.all([
                LivrariaClientModel.carregarLivros(),
                LivrariaClientModel.carregarCarrinho()
            ]);
            this.renderizarView();
        } catch (erro) {
            this.mostrarMensagem("Erro ao conectar ao servidor Back-end: " + erro.message, true);
        }
    },

    async acaoBuscar(event) {
        event.preventDefault();
        const termo = document.getElementById("inputBusca").value;
        await LivrariaClientModel.carregarLivros(termo);
        this.renderizarCatalogo();
    },

    async acaoAdicionarId(livroId) {
        try {
            await LivrariaClientModel.adicionarLivroPorId(livroId);
            this.mostrarMensagem("Livro adicionado ao carrinho!");
            this.renderizarCarrinho();
        } catch (erro) {
            this.mostrarMensagem(erro.message, true);
        }
    },

    async acaoScanIsbn(event) {
        event.preventDefault();
        const input = document.getElementById("inputIsbn");
        try {
            const livro = await LivrariaClientModel.escanearIsbn(input.value);
            input.value = "";
            this.mostrarMensagem(`Scan & Go: "${livro.titulo}" adicionado!`);
            this.renderizarCarrinho();
        } catch (erro) {
            this.mostrarMensagem(erro.message, true);
        }
    },

    async acaoRemover(index) {
        await LivrariaClientModel.removerDoCarrinho(index);
        this.renderizarCarrinho();
    },

    async acaoCheckoutPix(event) {
        event.preventDefault();
        const cliente = document.getElementById("inputCliente").value;
        try {
            await LivrariaClientModel.pagarComPix(cliente);
            this.mostrarMensagem("Pagamento PIX aprovado pelo servidor!");
            this.renderizarView();
        } catch (erro) {
            this.mostrarMensagem(erro.message, true);
        }
    },

    mostrarMensagem(texto, isErro = false) {
        const div = document.getElementById("alertaFeedback");
        div.style.display = "block";
        div.style.background = isErro ? "#f8d7da" : "#d4edda";
        div.style.color = isErro ? "#721c24" : "#155724";
        div.textContent = texto;
    },

    renderizarView() {
        this.renderizarCatalogo();
        this.renderizarCarrinho();
        this.renderizarRecibo();
    },

    renderizarCatalogo() {
        const container = document.getElementById("listaLivros");
        const livros = LivrariaClientModel.estado.livros;
        container.innerHTML = livros.map(l => `
            <div class="book-item">
                <div>
                    <strong>${l.titulo}</strong><br>
                    <small>${l.autor} • ${l.genero}</small><br>
                    <small>ISBN: <code>${l.isbn}</code> | Estoque: <b>${l.estoque}</b></small>
                    <p class="price">R$ ${l.preco.toFixed(2)}</p>
                </div>
                <button onclick="LivrariaClientController.acaoAdicionarId(${l.id})" ${l.estoque <= 0 ? "disabled" : ""}>
                    ${l.estoque > 0 ? "+ Adicionar ao Carrinho" : "Esgotado"}
                </button>
            </div>
        `).join("");
    },

    renderizarCarrinho() {
        const { itens, quantidade, subtotal } = LivrariaClientModel.estado.carrinho;
        document.getElementById("badgeContador").textContent = quantidade;
        document.getElementById("valorSubtotal").textContent = subtotal.toFixed(2);

        const lista = document.getElementById("listaCarrinho");
        if (itens.length === 0) {
            lista.innerHTML = `<p style="color:#7f8c8d;">O carrinho está vazio.</p>`;
            return;
        }
        lista.innerHTML = itens.map((item, idx) => `
            <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #eee;">
                <span>${item.titulo} (R$ ${item.preco.toFixed(2)})</span>
                <button class="btn-danger" onclick="LivrariaClientController.acaoRemover(${idx})">X</button>
            </div>
        `).join("");
    },

    renderizarRecibo() {
        const recibo = LivrariaClientModel.estado.ultimoRecibo;
        const box = document.getElementById("boxReciboQr");
        if (!recibo) {
            box.style.display = "none";
            return;
        }
        box.style.display = "block";
        box.innerHTML = `
            <strong>✅ SAÍDA LIBERADA (${recibo.data_hora})</strong><br>
            Cliente: ${recibo.cliente} | Total: R$ ${recibo.total.toFixed(2)}<br>
            <code>${recibo.qr_code}</code>
        `;
    }
};

window.addEventListener("DOMContentLoaded", () => LivrariaClientController.inicializar());
