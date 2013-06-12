# -*- coding: utf-8 -*-

print "model.__init__.py invoked!"

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ["user"]