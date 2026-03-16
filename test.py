import unittest
from starlette.testclient import TestClient
from app import app, users


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_get_users(self):
        response = self.client.get('/users')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, users)

    def test_delete_user(self):
        user_id = 546
        response = self.client.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'success'})
        self.assertIsNone(next((u for u in users if u['id'] == user_id), None))

    def test_delete_user_not_found(self):
        user_id = 999
        response = self.client.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
