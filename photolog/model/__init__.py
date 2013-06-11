# -*- coding: utf-8 -*-

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 
# engine = create_engine('sqlite:////Users/keatonh/project/database/flaskr', echo=False, convert_unicode=True)
#  
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

print "model.__init__.py invoked!"

Base = declarative_base()
# Base.query = DBManager.db_session.query_property()