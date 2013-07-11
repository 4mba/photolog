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
from flask import request, redirect, url_for, current_app, send_from_directory \
				, render_template, session
from werkzeug.utils import secure_filename

from photolog.database import DBManager
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.exif_reader import EXIFReader

from photolog.photolog_blueprint import photolog
from datetime import datetime
import uuid


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@photolog.route('/photo/upload')
@photolog.route('/photo/upload/<filename>')
@login_required
def upload_form(filename=None):
    return render_template('upload.html', filename=filename)


@photolog.route('/photo/upload_photo', methods=['POST'])
@login_required
def upload_photo():

    print 'uploading upload_photo size of upload_photo length : %s' % \
        current_app.config['MAX_CONTENT_LENGTH']

    userid = session['user_info'].username
    tag = request.form['tag']
    comment = request.form['memo']
    upload_photo = request.files['upload']
    filename = None
    filesize = 0

    # 파일 업로드시 발생하는 예외 처리
    try:
        if upload_photo and allowed_file(upload_photo.filename):
            # secure_filename은 한글 지원 안됨
            # filename = secure_filename(upload_photo.filename)
            ext = (upload_photo.filename).rsplit('.', 1)[1]
            filename = userid +'_'+ unicode(uuid.uuid4()) + '.' + ext
            upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            upload_photo.save(os.path.join(upload_folder, filename))
            filesize = os.stat(upload_folder+filename).st_size

        else:
            raise Exception("File uoload error : illegal file.")
    except Exception as e:
        print "Upload error : %s" % str(e)

    # EXIF 데이터 파잇ㅇ 예외 처리
    try :
        exif = EXIFReader(upload_folder + os.sep + filename)
        geotag_lat = exif.get_geotag_lat()
        geotag_lng = exif.get_geotag_lng()
        upload_date = datetime.today()
        taken_date = datetime.today()
        
        # 디버깅 데이터 확인을 위해 출력 (임시)
        exif.print_all()


    except Exception as e:
        print "EXIF dara parsing error : %s" % str(e)

        userid = request.form['userid']
        tag = request.form['tag']
        comment = request.form['comment']

    # DB에 저장할 때 발생하는 예외 처리
    try :
        photo = Photo(userid, tag, comment, filename, filesize, str(geotag_lat), str(geotag_lng), upload_date, taken_date)
        dao = DBManager.db_session
        dao.add(photo)
        dao.commit()

    except Exception as e:
        print "Upload data error : %s" % str(e)

    return render_template('entry_all.html', name=filename)


@photolog.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
