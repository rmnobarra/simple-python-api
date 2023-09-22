# simple python api with swagger and test

Try:

```bash
python app.py
```

Your API is available on http://localhost:5000. You can do a test call to the following API endpoints GET /users and DELETE /users using your favorite tool.

Theres a swagger in /apidocs path too.

## Docker 

```bash
docker build -t simple-python-api .
```

```bash
docker run -p 5000:5000 simple-python-api
```