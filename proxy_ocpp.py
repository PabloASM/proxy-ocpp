from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

POWER_AUTOMATE_URL = "https://prod-239.westeurope.logic.azure.com:443/workflows/baefd2f4070f4968823318d3f5dfca3a/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=BWLx5HiJk0WqHruCeGxuA1wIbuvrrIRvKKhsowsqr88"

# Endpoint GET para verificar estado
@app.route('/', methods=['GET'])
def status():
    return "Proxy OCPP en funcionamiento"

# Endpoint PUT para recibir archivos, compatible con múltiples tipos de cargador
@app.route('/', defaults={'path': ''}, methods=['PUT'])
@app.route('/<path:path>', methods=['PUT'])
def receive_file(path):
    print(f"Petición PUT recibida en ruta: {path}")
    print("Headers:", dict(request.headers))

    file_data = None

    # Detectar y manejar el tipo de contenido
    if request.content_type.startswith("multipart/form-data"):
        if 'file' in request.files:
            uploaded_file = request.files['file']
            file_data = uploaded_file.read()
            print(f"Archivo recibido con nombre: {uploaded_file.filename}")
        else:
            return Response("No se encontró archivo en 'file'", status=400)
    else:
        file_data = request.data

    headers = {"Content-Type": "application/zip"}
    response = requests.post(POWER_AUTOMATE_URL, headers=headers, data=file_data)

    print("Respuesta de Power Automate:", response.status_code, response.text)
    if response.status_code in [200, 202]:
        return Response("Archivo reenviado correctamente.", status=200)
    else:
        return Response(f"Error reenviando a Power Automate: {response.text}", status=500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

