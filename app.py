from flask import Flask, jsonify, request, abort, Response
from flasgger import Swagger
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from jaeger_client import Config
from flask_opentracing import FlaskTracer
import time
import logging
import graypy
import os


app = Flask(__name__)
swagger = Swagger(app)

# Configurando o Jaeger Tracing
jaeger_config = Config(
    config={
        'sampler': {'type': 'const', 'param': 1},
        'local_agent': {'reporting_host': 'jaeger', 'reporting_port': 5775},
        'logging': True,
    },
    service_name='simple_python_api',
    validate=True,
)
jaeger_tracer = jaeger_config.initialize_tracer()
tracer = FlaskTracer(jaeger_tracer, True, app)

# Configurando o logging
logging.basicConfig(level=logging.INFO)

# Configurando o graypy
graylog_host = os.environ.get('GRAYLOG_HOST', 'localhost')
handler = graypy.GELFUDPHandler(graylog_host, 12201)
logging.getLogger().addHandler(handler)

# Definindo métricas
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # When: Quando a requisição foi feita
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    # Where: De onde a requisição foi feita
    remote_addr = request.remote_addr
    # What: O que aconteceu
    method = request.method
    url = request.url
    # Who: Quem fez a requisição
    user_agent = request.user_agent.string
    # Calculando a duração da requisição e arredondando para 3 casas decimais
    duration = round(time.time() - request.start_time, 3)
    # Status da resposta
    status_code = response.status_code
    
    # Logando as informações
    logging.info('%s | %s | %s | %s | %s | Status: %s | Duration: %s s', timestamp, remote_addr, method, url, user_agent, status_code, duration)
    
    # Incrementando o contador de requisições
    REQUESTS.labels(method, url, status_code).inc()
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
    """
    Retorna a lista de usuários
    ---
    responses:
      200:
        description: Lista de usuários
        examples:
          [{"id": 546, "username": "John"}, {"id": 894, "username": "Mary"}, {"id": 326, "username": "Jane"}]
    """
    if tracer:
        with tracer.start_span('get_users') as span:
            return jsonify(users)
    else:
        app.logger.error("Tracer not initialized")
        return jsonify(users)
    
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deleta um usuário pelo ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado com sucesso
        examples:
          {"result": "success"}
      404:
        description: Usuário não encontrado
    """
    with tracer.trace('delete_user'):
        user = next((user for user in users if user['id'] == user_id), None)
        if user is None:
            abort(404)
        users.remove(user)
        return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
