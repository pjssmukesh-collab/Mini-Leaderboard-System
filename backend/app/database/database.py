# app/database/database.py
# ──────────────────────────────────────────────
# Database Connection & Session Management
#
# WHAT THIS FILE DOES:
# 1. Creates the "engine" — the connection to your SQLite database file
# 2. Creates a "session factory" — gives you a fresh session each time
#    your API needs to talk to the database
# 3. Provides a "get_db()" function that FastAPI uses to inject
#    a database session into your route handlers
#
# ANALOGY:
# - Engine = the power cable connecting your app to the database
# - Session = a single conversation with the database (open → query → close)
# - Base = the blueprint class that all your models inherit from
# ──────────────────────────────────────────────

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# ──────────────────────────────────────────────
# 1. Create the Engine
# ──────────────────────────────────────────────
# The engine is the starting point for any SQLAlchemy application.
# It manages the connection pool to the database.
#
# connect_args={"check_same_thread": False}:
#   SQLite by default only allows one thread to use it.
#   FastAPI is async/multi-threaded, so we disable this check.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,  # When True, prints all SQL queries (helpful for learning!)
)


# ──────────────────────────────────────────────
# 2. Enable Foreign Keys for SQLite
# ──────────────────────────────────────────────
# SQLite does NOT enforce foreign keys by default!
# This listener runs "PRAGMA foreign_keys=ON" every time
# a new connection is opened, so relationships are enforced.
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ──────────────────────────────────────────────
# 3. Create the Session Factory
# ──────────────────────────────────────────────
# A "session" is like a notebook where you write down all the
# database operations you want to do, then "commit" them all at once.
#
# autocommit=False: You decide when to save changes
# autoflush=False:  Don't automatically push changes to DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ──────────────────────────────────────────────
# 4. Create the Base Class
# ──────────────────────────────────────────────
# Every database model (User, Event, etc.) will inherit from this.
# It's what connects your Python classes to actual database tables.
Base = declarative_base()


# ──────────────────────────────────────────────
# 5. Dependency: get_db()
# ──────────────────────────────────────────────
# FastAPI uses "dependencies" to inject things into route handlers.
# This function:
#   1. Opens a new database session
#   2. Gives it to your route handler to use
#   3. Automatically closes it when the request is done
#
# Usage in a route (coming in future prompts):
#   @app.get("/users")
#   def get_users(db: Session = Depends(get_db)):
#       return db.query(User).all()
def get_db():
    db = SessionLocal()
    try:
        yield db  # Give the session to the route handler
    finally:
        db.close()  # Always close when done, even if there's an error


# ──────────────────────────────────────────────
# 6. Database Initialization
# ──────────────────────────────────────────────
def init_db():
    """
    Creates all database tables defined in the SQLAlchemy models.
    Safe to call multiple times (creates tables only if they don't exist).
    """
    import app.models  # noqa: F401 - ensures all models are registered on Base
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drops all database tables. Useful for test suites or resets.
    """
    import app.models  # noqa: F401
    Base.metadata.drop_all(bind=engine)

