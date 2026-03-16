from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

users = [
    {'id': 546, 'username': 'John'},
    {'id': 894, 'username': 'Mary'},
    {'id': 326, 'username': 'Jane'}
]


@app.get('/users')
def get_users():
    return users


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404)
    users.remove(user)
    return {'result': 'success'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
