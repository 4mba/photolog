# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from photolog.model import Base

	
class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	username = Column(String(50), unique=True)
	password = Column(String(120), unique=True)
	
	def __init__(self, name=None, password=None):
		self.username = name
		self.password = password
		
	def __repr__(self):
		return '<User %r %r>' % (self.username, self.password)
	