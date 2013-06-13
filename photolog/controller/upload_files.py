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
# from werkzeug.utils import secure_filename

from .. import photolog
from .login import login_required

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@photolog.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
	print 'upload_file size of file length : %s' % current_app.config['MAX_CONTENT_LENGTH']
	if request.method == 'POST':
		file = request.files['file']
			
		if file and allowed_file(file.filename):
	# 		filename = secure_filename(file.filename)
			filename = file.filename
			file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('.upload_file', filename=filename))
	else:
		return render_template('upload.html', filename=None)


@photolog.route('/upload/<filename>')
@login_required
def uploaded_file(filename):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], 	filename)
