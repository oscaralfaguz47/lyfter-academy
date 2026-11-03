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
4. Run the API
```
flask run --debug
```
5. Set up Alembic, from the project root, run the following:
```
alembic init db/migrations
```
6. Verify if all tables exist
```
python -m db.init_db
```
7. Make a user 'Admin'
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