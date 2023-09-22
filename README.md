# simple python api

Run:

```bash
python api.py
```

Your API is available on http://localhost:5000. You can do a test call to the following API endpoints GET /users and DELETE /users using your favorite tool (here, Insomnia) and see the returned response:


docker build -t simple-python-api .

docker run -p 5000:5000 simple-python-api
