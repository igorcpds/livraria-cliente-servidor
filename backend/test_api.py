from app import app

def test_api_cliente_servidor_fluxo_completo():
    client = app.test_client()

    # 1. Cliente consulta catálogo (GET /api/livros)
    res_livros = client.get("/api/livros")
    assert res_livros.status_code == 200
    assert len(res_livros.get_json()) >= 4

    # 2. Cliente faz Scan & Go por ISBN (POST /api/carrinho/scan)
    res_scan = client.post("/api/carrinho/scan", json={"isbn": "9780451524935"})
    assert res_scan.status_code == 201
    assert res_scan.get_json()["carrinho"]["subtotal"] == 45.00

    # 3. Cliente finaliza pagamento PIX (POST /api/checkout/pix)
    res_pix = client.post("/api/checkout/pix", json={"cliente": "Igor"})
    assert res_pix.status_code == 201
    assert "QR-CS-PIX-" in res_pix.get_json()["qr_code"]
