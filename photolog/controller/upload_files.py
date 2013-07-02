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
				, render_template
from werkzeug.utils import secure_filename

from photolog.database import DBManager
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.exif_reader import EXIFReader

from .. import photolog
from .login import login_required
from datetime import datetime


ALLOWED_EXTENSIONS = set(['txt', 'doc', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@photolog.route('/upload/')
@photolog.route('/upload/<filename>')
@login_required
def upload(filename=None):
		return render_template('upload.html', filename=filename)

			
@photolog.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
				
	print 'uploading file size of file length : %s' % \
		current_app.config['MAX_CONTENT_LENGTH']
	try:
		file = request.files['file']

		if file and allowed_file(file.filename):
			#secure_filename은 한글 지원 안됨
			#filename = secure_filename(file.filename)
			filename = file.filename
			print "filename : %s" % filename
			filename = file.filename
			upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
			print "root_path : %s" % current_app.root_path
			print "upload_folder : %s" % upload_folder
			file.save(os.path.join(upload_folder, filename))
			
			userid = request.form['userid']			
			tag = request.form['tag']			
			comment = request.form['comment']			
			exif = EXIFReader(upload_folder + filename)
			geotag_lat = exif.get_geotag_lat()
			geotag_lng = exif.get_geotag_lng()
			upload_date = datetime.today()
			taken_date = datetime.today()
            
			print "geotag_lat: %s" % geotag_lat 
           
			photo = Photo(userid, tag, comment, geotag_lat, geotag_lng, upload_date, taken_date)
			DBManager.db_session.add(photo)
			DBManager.db_session.commit()

			return render_template('main.html', name=filename)
		else:
			raise Exception("No file or support file extensions")
	except Exception as e:
		print "Upload error : %s" % str(e)
        render_template('500.html')


@photolog.route('/download/<filename>')
@login_required
def download_file(filename):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
