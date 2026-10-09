from flask import Flask, current_app, g
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Without NAMING_CONVENTIONS SQLAlchemy doesn't know the names that PostgreSQL creates, when Alembric needs to delete or update a constraint it should know the name.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    """ Parent class of every model """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)

def init_db(app: Flask) -> None:
    """ Creates the engine ans session factory and close sessions after each request. """
    connect_args = {} # An extra dict options that we pass to the driver (psycopg), every time a connection is open it starts empty.
    schema = app.config.get("DB_SCHEMA")
    if schema:
        connect_args["options"] = f"-c search_path={schema}" # search_path tells to Postgres "search the tables first in this schema"

    # create_engine is lazy, it still is not connected to Postgres, the first real connection happens when a user executes a request
    # create_engine creates a pool that by default saves up 5 open and reusable connections.
    engine = create_engine(  
        app.config["DATABASE_URL"],
        pool_pre_ping=True, # Before using a pool connection, it verifies that it's alive, this avoids errors when Postgres resets
        connect_args=connect_args,
    )
    # With app.extensions we save the engine in the app, this helps the tests to create their own app with their own base without crashes
    app.extensions["db_engine"] = engine

    # Here with expire_on_commit=False, after the commit() we can read the object attributes to return the JSON without another request
    # sessionmaker() creates a factory and every time we call factory() it returns a new session with all the configurations we made.
    app.extensions["db_session_factory"] = sessionmaker(bind=engine, expire_on_commit=False)

    # Flask calls _close_session always after the request ends, even if there's an error, this way, no connections are left open
    app.teardown_appcontext(_close_session)

# get_session() is executed in every session, it creates the session and reuses it in all the request
def get_session() -> Session:
    if "db_session" not in g: # g is Flask storage by request, if there's no an existing request, current_app.extensions[] search the factory and creates a new one
        g.db_session = current_app.extensions["db_session_factory"]()
    return g.db_session # Returns the new or existing request

# Here Flask always passes an argument, the exception if fails or None if was Ok.
def _close_session(exception: BaseException | None) -> None:
    session = g.pop("db_session", None) # g.poop() takes of the session and returns it.
    if session is not None: # The value of session if there's anyone is "None", here we avoid an error if the request never calls get_session().
        session.close() # Here rolls back anything not committed and returns the connection to the pool, it doesn't close it, it leaves it ready for use.