# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print "database module invoked!"
# engine = create_engine('sqlite:////Users/keatonh/project/database/flaskr', echo=False, convert_unicode=True)
# 
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# 
# Base = declarative_base()
# Base.query = db_session.query_property()

class DBManager:
    db_session = None
        
    @staticmethod
    def init(db_url):
        engine = create_engine(db_url, echo=True, convert_unicode=True) 
        DBManager.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    

# def init_db():
#     from photolog.model import *
#     Base.metadata.create_all(bind=engine)