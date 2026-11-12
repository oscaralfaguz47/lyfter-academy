## Commands to get started
1. Create an isolated environment inside the project (only once)
```
python3 -m venv .venv
```
2. Activate the created isolated environment (every time you open a new terminal)
```
source .venv/bin/activate
```
3. Install everything
```
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```
4. Generate de private and public .pem files
```
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out keys/jwt_private.pem
openssl rsa -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem
```
5.Create the Redis container (only once, Docker must be running)
```
docker run -d --name pet-ecommerce-redis-cache -p 127.0.0.1:6379:6379 redis:8-alpine \
  redis-server --save "" --appendonly no --maxmemory 128mb --maxmemory-policy volatile-lru
```
6. Run the API
```
flask run --debug
```
7. Set up Alembic, from the project root, run the following:
```
alembic init db/migrations
```
8. Verify if all tables exist
```
python -m db.init_db
```
9. Make a user 'Admin'
```
flask --app app promote-admin <the user's email>
```


## Commands while programming
1. Generate migrations
```
alembic revision --autogenerate -m "create users table"
```
2. Apply the generated migration in the DB
```
alembic upgrade head
```
3. List existing roles with their permissions
```
flask --app app permissions
```
4. Start Redis (every time we open the project)
```
docker start redis-cache
```
5. Monitor every command Redis receives
```
docker exec -it redis-cache redis-cli MONITOR
```

## Commands to execute tests
1. Run all existing tests
```
pytest -v
```
2. Run tests for a specific file
```
pytest tests/<routes or unit>/<name of the file>
```
3. Run a specific test
```
pytest tests/<routes or unit>/<name of the file>::<name of the test>
```