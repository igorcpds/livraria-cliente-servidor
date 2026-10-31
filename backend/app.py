import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes import api_bp

app = Flask(__name__)
# Ativa CORS para permitir que o Front-end separado consuma a API
CORS(app)

app.register_blueprint(api_bp)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Backend Online", "arquitetura": "Cliente-Servidor"}), 200

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=True)
