# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

print "database module invoked!"

class DBManager:
    db_session = None
    engine = None
        
    @staticmethod
    def init(db_url):
        print "DB_URL : %s" % db_url
        DBManager.engine = create_engine(db_url, echo=True, convert_unicode=True) 
        DBManager.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=DBManager.engine))
    
    @staticmethod
    def init_db():
        from photolog.model import Base
        Base.metadata.create_all(bind=DBManager.engine)