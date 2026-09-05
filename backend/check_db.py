from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/smart_budget_ai"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(
        text("DELETE FROM statements WHERE user_id = :uid"),
        {"uid": "07081195-8f6f-42b2-a534-09c8e5c77d2e"}
    )
    conn.commit()
    print("Deleted all local test statements.")