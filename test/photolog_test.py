# -*- coding: utf-8 -*-
"""
    test.photolog_test
    ~~~~~~~~~~~~~~~~~~~

    photolog 어플리케이션의 단위 테스트 모

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""

import os
import unittest

from photolog import create_app

class PhotologTest(unittest.TestCase):

    photolog_app = None
    
    def setUp(self):
        self.photolog_app = create_app('/Users/keatonh/project/photolog/test/config.cfg')
        self.photolog_app.testing = True
        self.app = self.photolog_app.test_client()


    def register_user(self, username, email, password, password_confirm):
        return self.app.post('/user/regist', data=dict(username=username, 
                                                    email=email,
                                                    password=password,
                                                    password_confirm=password_confirm),
                               follow_redirects=True)
    
    def test_register_user(self):
        rv = self.register_user(username='keaton', email='keaton',
                                password='1234', password_confirm='1234')
        
#         print "rv.status : %s /rv.status_code : %s" % (rv.status, rv.status_code)
        assert rv.status_code == 200 
        
        assert('로그인 하기' in rv.data)
        
        
    def test_log_in_error_user_not_exist(self):
        rv = self.app.post('/user/login', data=dict(username='keaton', 
                                                    password='keaton',
                                                    next=''),
                               follow_redirects=True)
        
        assert('User does not exist!' in rv.data)
    
     
        

    def tearDown(self):
        os.remove(self.photolog_app.config['LOG_FILE_PATH'])
        os.remove(self.photolog_app.config['DB_FILE_PATH'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()