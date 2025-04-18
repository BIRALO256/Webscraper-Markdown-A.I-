from sqlalchemy import create_engine
from service.config import config

engine = create_engine(config.postgres_uri)

# Define ORM models or simple insert utilities