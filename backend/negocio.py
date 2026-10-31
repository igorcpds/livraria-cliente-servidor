from datetime import datetime
from dados import db

class LivrariaNegocio:
    @staticmethod
    def consultar_catalogo(termo: str = ""):
        livros = db.listar_livros()
        if not termo:
            return livros
        t = termo.lower()
        return [l for l in livros if t in l["titulo"].lower() or t in l["autor"].lower()]

    @staticmethod
    def obter_estado_carrinho():
        subtotal = sum(item["preco"] for item in db.carrinho)
        return {
            "itens": db.carrinho,
            "quantidade": len(db.carrinho),
            "subtotal": round(subtotal, 2)
        }

    @staticmethod
    def adicionar_por_id(livro_id: int):
        livro = db.buscar_por_id(livro_id)
        if not livro:
            raise ValueError("Livro não encontrado.")
        if livro["estoque"] <= 0:
            raise ValueError("Livro sem estoque disponível.")
        db.adicionar_carrinho(livro)
        return LivrariaNegocio.obter_estado_carrinho()

    @staticmethod
    def adicionar_por_isbn(isbn: str):
        livro = db.buscar_por_isbn(isbn)
        if not livro:
            raise ValueError(f"ISBN '{isbn}' não encontrado no catálogo.")
        if livro["estoque"] <= 0:
            raise ValueError("Livro sem estoque disponível.")
        db.adicionar_carrinho(livro)
        return {"livro_reconhecido": livro, "carrinho": LivrariaNegocio.obter_estado_carrinho()}

    @staticmethod
    def remover_item(index: int):
        db.remover_carrinho(index)
        return LivrariaNegocio.obter_estado_carrinho()

    @staticmethod
    def finalizar_checkout_pix(cliente: str = "Cliente Loja"):
        if not db.carrinho:
            raise ValueError("O carrinho está vazio.")

        for item in db.carrinho:
            if item["estoque"] <= 0:
                raise ValueError(f"Estoque esgotado para '{item['titulo']}'.")
        for item in db.carrinho:
            item["estoque"] -= 1

        total = sum(i["preco"] for i in db.carrinho)
        titulos = ", ".join(i["titulo"] for i in db.carrinho)
        recibo = {
            "id": len(db.recibos) + 1,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cliente": cliente or "Cliente Anónimo",
            "itens": titulos,
            "total": round(total, 2),
            "qr_code": f"QR-CS-PIX-{int(datetime.now().timestamp())}"
        }
        db.salvar_recibo(recibo)
        db.limpar_carrinho()
        return recibo
