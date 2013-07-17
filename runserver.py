# -*- coding: utf-8 -*-
"""
    runserver
    ~~~~~~~~~

    로컬 테스트를 위한 개발 서버 실행 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


if __name__ == '__main__':
    print "starting test server..."
    from photolog import create_app
    create_app().run(host='0.0.0.0', port=5000)

