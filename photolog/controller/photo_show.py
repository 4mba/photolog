# -*- coding: utf-8 -*-
"""
    photolog.controller.photo_show
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    업로드된 사진을 보여준다.
    
    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import os
from flask import request, redirect, url_for, current_app, send_from_directory \
				, render_template, session
from werkzeug.utils import secure_filename

from photolog.database import dao
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.exif_reader import EXIFReader

from photolog.photolog_blueprint import photolog
from datetime import datetime

from photolog.photolog_logger import Log

import uuid


# 파일 사이즈를 일기 편한포맷으로 변경해주는 함수
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')



@photolog.route('/photo/show/')
@login_required
def show_all():    
    return render_template('entry_all.html', 
                           photos=dao.query(Photo).order_by(Photo.upload_date.desc()).all(), 
                           sizeof_fmt=sizeof_fmt)


@photolog.route('/photo/download/<photolog_id>')
@login_required
def download_photo(photolog_id):
    photo = dao.query(Photo).filter_by(id=photolog_id).first()
    realpath = photolog.root_path + os.sep + current_app.config['UPLOAD_FOLDER']
    
    return send_from_directory(realpath, photo.filename, as_attachment=True , mimetype='image/jpg')


@photolog.route('/photo/show/map')
@login_required
def show_map(): 
    try:
        userid = session['user_info'].id
        Log.debug(userid)
        return render_template('show_map.html', photos=dao.query(Photo).filter_by(userid=userid).order_by(Photo.taken_date.desc()).all())
    except Exception as e:
        Log.error(str(e))
        raise e
    



