from databases import Database
from sqlalchemy.ext.declarative import declarative_base

from api.core.config import DATABASE_URL

database = Database(DATABASE_URL)
Base = declarative_base()