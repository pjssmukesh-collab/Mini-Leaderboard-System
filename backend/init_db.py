# init_db.py
# ──────────────────────────────────────────────
# Standalone SQLite Database Initializer
# Run with: python init_db.py
# ──────────────────────────────────────────────

from app.database import init_db, engine
from sqlalchemy import inspect


def main():
    print("Connecting to SQLite database and creating tables...")
    init_db()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Successfully created {len(tables)} tables:")
    for t in sorted(tables):
        print(f"  - {t}")
    print("\nDatabase initialization complete.")


if __name__ == "__main__":
    main()
