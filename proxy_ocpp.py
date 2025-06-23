from flask import Flask, request, Response
import requests, os

app = Flask(__name__)
POWER_AUTOMATE_URL = os.getenv("POWER_AUTOMATE_URL")  # idealmente configurable

@app.route('/', methods=['GET'])
def status():
    return "Proxy OCPP funcionando"

@app.route('/', defaults={'path': ''}, methods=['PUT'])
@app.route('/<path:path>', methods=['PUT'])
def receive_file(path):
    file_data = request.get_data()
    # Toma el Content-Type si viene, si no lo fuerza a binario
    content_type = request.headers.get('Content-Type', 'application/octet-stream')
    headers = {"Content-Type": content_type}

    print("Recibido PUT en ruta:", path, "Content-Type:", content_type)
    response = requests.post(POWER_AUTOMATE_URL, headers=headers, data=file_data)
    print("POST a Power Automate:", response.status_code, response.text)

    if response.status_code in (200, 202):
        return Response("Reenviado correctamente", status=200)
    return Response("Error reenviando", status=500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
