import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pwd=quote_plus("FleetUser@2024!")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg://fleet_user:{pwd}@localhost:5432/fms"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)