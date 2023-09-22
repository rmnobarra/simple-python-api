from flask import Flask, jsonify, request, abort
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

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
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)
    users.remove(user)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
