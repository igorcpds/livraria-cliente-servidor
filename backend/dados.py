class LivrariaDados:
    def __init__(self):
        self.livros = [
            {"id": 1, "titulo": "1984", "autor": "George Orwell", "genero": "Ficção Científica", "isbn": "9780451524935", "preco": 45.00, "estoque": 10},
            {"id": 2, "titulo": "O Guia do Mochileiro das Galáxias", "autor": "Douglas Adams", "genero": "Ficção Científica", "isbn": "9788530601492", "preco": 39.90, "estoque": 5},
            {"id": 3, "titulo": "Código Limpo (Clean Code)", "autor": "Robert C. Martin", "genero": "Tecnologia", "isbn": "9788576082675", "preco": 89.90, "estoque": 8},
            {"id": 4, "titulo": "Arquitetura Limpa", "autor": "Robert C. Martin", "genero": "Tecnologia", "isbn": "9788550804606", "preco": 79.50, "estoque": 4}
        ]
        self.carrinho = []
        self.recibos = []

    def listar_livros(self):
        return self.livros

    def buscar_por_id(self, livro_id: int):
        return next((l for l in self.livros if l["id"] == int(livro_id)), None)

    def buscar_por_isbn(self, isbn: str):
        return next((l for l in self.livros if l["isbn"] == str(isbn).strip()), None)

    def adicionar_carrinho(self, item: dict):
        self.carrinho.append(item)

    def remover_carrinho(self, index: int):
        if 0 <= index < len(self.carrinho):
            return self.carrinho.pop(index)
        return None

    def limpar_carrinho(self):
        self.carrinho.clear()

    def salvar_recibo(self, recibo: dict):
        self.recibos.append(recibo)
        return recibo


db = LivrariaDados()
