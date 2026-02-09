import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# Configurações - Use variáveis de ambiente em produção
WEBHOOK_URL = os.environ.get("JIRA_WEBHOOK_URL")
TIMEOUT_SECONDS = 60

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar():
    user_input = request.json.get("description", "").strip()
    
    if not user_input:
        return jsonify({"error": "A descrição não pode estar vazia."}), 400

    try:
        payload = {"description": user_input}
        response = requests.post(WEBHOOK_URL, json=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        
        data = response.json()
        # Garante que a chave 'resposta' existe no retorno do n8n
        resultado = data.get("resposta", "Nenhum resultado retornado pelo analista.")
        return jsonify({"resultado": resultado})

    except requests.exceptions.Timeout:
        return jsonify({"error": "O serviço de análise demorou muito para responder."}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Não foi possível conectar ao servidor de automação."}), 502
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)