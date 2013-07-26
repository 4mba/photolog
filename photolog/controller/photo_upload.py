# -*- coding: utf-8 -*-
"""
    photolog.controller.upload_files
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    파일 업로드 모듈.
    사진을 어플리케이션 서버의 임시 디렉터리에 저장함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import os
from flask import request, redirect, url_for, current_app, render_template, session
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

from photolog.database import dao
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.photolog_logger import Log
from photolog.photolog_blueprint import photolog
from PIL import Image


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@photolog.route('/photo/upload')
@photolog.route('/photo/upload/<filename>')
@login_required
def upload_form(filename=None):
    return render_template('upload.html', filename=filename)


@photolog.route('/photo/upload', methods=['POST'])
@login_required
def upload_photo():

    user_id = session['user_info'].id
    username = session['user_info'].username
    tag = request.form['tag']
    comment = request.form['memo']
    lat = request.form['lat']
    lng = request.form['lng']
    upload_date = datetime.today()

    try:
        taken_date = datetime.strptime(request.form['date'], "%Y:%m:%d %H:%M:%S");
    except :
        taken_date = datetime.today()
    
    upload_photo = request.files['upload']
    filename = None
    filesize = 0
    filename_orig = upload_photo.filename

    try:
        if upload_photo and allowed_file(upload_photo.filename):
            # secure_filename은 한글 지원 안됨
            
            ext = (upload_photo.filename).rsplit('.', 1)[1]
            filename = secure_filename(username +'_'+ unicode(uuid.uuid4())+"."+ext)
            
            upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            upload_photo.save(os.path.join(upload_folder, filename))
            
            filesize = os.stat(upload_folder+filename).st_size
            
            make_thumbnails(filename)
            

        else:
            raise Exception("File upload error : illegal file.")

    except Exception as e:
        Log.error(str(e))
        raise e

    try :
        photo = Photo(user_id, tag, comment, filename_orig, filename, filesize, lat, lng, upload_date, taken_date)
        dao.add(photo)
        dao.commit()

    except Exception as e:
        dao.rollback()
        Log.error("Upload DB error : " + str(e))
        raise e

    return redirect(url_for('.show_all'))



@photolog.route('/photo/modify/<photolog_id>')
@login_required
def modify(photolog_id):
    photo = dao.query(Photo).filter_by(id=photolog_id).first()
    
    return render_template('upload.html', photo=photo)




def make_thumbnails(filename):
    
    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])

    original_file = upload_folder+filename
    target_name = upload_folder+"thumb_"+filename
    
    try:
        im = Image.open(original_file)
        im = im.convert('RGB')
        im.thumbnail((300,300), Image.ANTIALIAS)
        im.save(target_name)

    except Exception as e:
        Log.error("Thumbnails creation error : " + target_name+" , "+str(e))
        raise e
    

@photolog.route('/iphone')
def iphone():
    return render_template('iphone.html')

