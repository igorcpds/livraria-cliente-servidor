// Altere esta URL para o link do seu Back-end em produção no Exercício 8.6
const API_BASE_URL = window.BACKEND_URL || "http://127.0.0.1:5000/api";

const LivrariaClientModel = {
    estado: {
        livros: [],
        carrinho: { itens: [], quantidade: 0, subtotal: 0.0 },
        ultimoRecibo: null
    },

    async carregarLivros(termo = "") {
        const url = termo ? `${API_BASE_URL}/livros?q=${encodeURIComponent(termo)}` : `${API_BASE_URL}/livros`;
        const resp = await fetch(url);
        this.estado.livros = await resp.json();
        return this.estado.livros;
    },

    async carregarCarrinho() {
        const resp = await fetch(`${API_BASE_URL}/carrinho`);
        this.estado.carrinho = await resp.json();
        return this.estado.carrinho;
    },

    async adicionarLivroPorId(livroId) {
        const resp = await fetch(`${API_BASE_URL}/carrinho/adicionar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ livro_id: livroId })
        });
        const dados = await resp.json();
        if (!resp.ok) throw new Error(dados.erro || "Erro ao adicionar livro");
        this.estado.carrinho = dados;
        return dados;
    },

    async escanearIsbn(isbn) {
        const resp = await fetch(`${API_BASE_URL}/carrinho/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ isbn })
        });
        const dados = await resp.json();
        if (!resp.ok) throw new Error(dados.erro || "ISBN não encontrado");
        this.estado.carrinho = dados.carrinho;
        return dados.livro_reconhecido;
    },

    async removerDoCarrinho(index) {
        const resp = await fetch(`${API_BASE_URL}/carrinho/remover/${index}`, {
            method: "DELETE"
        });
        this.estado.carrinho = await resp.json();
        return this.estado.carrinho;
    },

    async pagarComPix(cliente) {
        const resp = await fetch(`${API_BASE_URL}/checkout/pix`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cliente })
        });
        const dados = await resp.json();
        if (!resp.ok) throw new Error(dados.erro || "Falha no checkout");
        this.estado.ultimoRecibo = dados;
        await this.carregarCarrinho();
        await this.carregarLivros();
        return dados;
    }
};
