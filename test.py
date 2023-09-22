import unittest
from flask import json
from app import app, users  # Importe a aplicação e a lista de usuários

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_users(self):
        response = self.app.get('/users')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, users)  # Verifique se a resposta corresponde à lista de usuários

    def test_delete_user(self):
        user_id = 546  # ID de um usuário existente
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'result': 'success'})
        self.assertIsNone(next((user for user in users if user['id'] == user_id), None))  # Verifique se o usuário foi removido da lista

    def test_delete_user_not_found(self):
        user_id = 999  # ID de um usuário inexistente
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
