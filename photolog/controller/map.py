# -*- coding: utf-8 -*-
"""
    photolog.controller.map
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    사진과 구글지도를 맵핑을 제공해 주는 모듈

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps

from photolog.photolog_blueprint import photolog
from photolog.database import DBManager
from photolog.model.user import User
   
@photolog.route('/show/entry/<entry_id>')
def show_entry(entry_id):
    """ entry_id 에 해당하는 내용을 DB에서 읽어와서 json 타입으로 리턴한다."""

    #: entry_id에 해당하는 값을 DB에서 가지고 와서 담는다.
    result = list()



    #: photolog.model.entry




    return render_template('main_maptest.html',json.dump(result));

