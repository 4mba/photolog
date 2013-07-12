# -*- coding: utf-8 -*-
"""
    photolog.model.photo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    photolog 어플리케이션을 사용할 사용자 정보에 대한 model 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from photolog.model.user import User

from photolog.model import Base


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    userid = Column(String(50), ForeignKey(User.id))
    tag = Column(String(100), unique=False)
    comment = Column(String(400), unique=False)
    filename = Column(String(400), unique=False)
    filesize = Column(Integer, unique=False)
    geotag_lat = Column(String(50), unique=False)
    geotag_lng = Column(String(50), unique=False)
    upload_date = Column(DateTime, unique=False)
    taken_date = Column(DateTime, unique=False)

    def __init__(self, userid, tag, comment, filename, filesize, geotag_lat, geotag_lng, upload_date, taken_date):
        self.userid = userid
        self.tag = tag
        self.comment = comment
        self.filename = filename
        self.filesize = filesize
        self.geotag_lat = geotag_lat
        self.geotag_lng = geotag_lng
        self.upload_date = upload_date
        self.taken_date = taken_date

    def __repr__(self):
        return '<Photo %r %r>' % (self.userid, self.upload_date)
