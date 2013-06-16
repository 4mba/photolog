# -*- coding: utf-8 -*-
"""
    runserver
    ~~~~~~~~~

    로컬 테스트를 위한 개발 서버 실행 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""

import os
    
if __name__ == '__main__':
    print "starting test server..."
    port = int(os.environ.get('PORT', 5000))
    from photolog import create_app
    print "creating photolog..."
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)

