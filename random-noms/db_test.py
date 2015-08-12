from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem, User
from db_link import getDBLink

# init SQLAlchemy
Base = declarative_base()
dblink = getDBLink()
engine = create_engine(dblink)
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

