# -*- coding: utf-8 -*-
"""
   photolog.py
    ~~~~~~~~~~~~~~

    JPEG 사진에서 EXIF(교환 이미지 파일 형식, EXchangable Image File format)를 이용하여,
    PhotoLog에서 사용할 위치기반 정보를 얻어 온다.

    :copyright: (c) 2013 by liks79 [http://www.github.com/liks79]
    :license: MIT LICENSE 2.0, see license for more details.
"""

import os
    
if __name__ == '__main__':
    print "starting photolog..."
    port = int(os.environ.get('PORT', 5000))
    from photolog import create_app
    print "creating photolog..."
    app = create_app()
    app.run(host='0.0.0.0', port=port)

