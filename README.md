
# Test task of Comagic
Implementations of a simple API.
## Run it
Install requirements: 

```$pip install -r requirements.txt```


Add to enviroment:
- `Debug=False`

Run app: 

```$python wsgi.py```

## Run test
Run tests:

```$python -m pytest --cov-report term --cov=api_app```