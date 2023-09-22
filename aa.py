from flask import Flask, jsonify, request, abort, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Definindo métricas
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def increment_request_count(response):
    request_latency = time.time() - request.start_time
    REQUESTS.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

users = [
    {'id': 546, 'username': 'John'},
    {'id': 894, 'username': 'Mary'},
    {'id': 326, 'username': 'Jane'}
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)
    users.remove(user)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
