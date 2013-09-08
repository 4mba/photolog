# -*- coding: utf-8 -*-
"""
    photolog.controller.twitter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    트위터와 OAUTH 연동하기 위한 모듈
    
    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import request, redirect, url_for, current_app, send_from_directory \
				, render_template, session
from sqlalchemy import or_

from photolog.database import dao
from photolog.controller.login import login_required
from photolog.controller.photo_show import photo_realpath
from photolog.controller.photo_show import photo_comment
from photolog.photolog_blueprint import photolog
from photolog.photolog_logger import Log
from twython import Twython


# 트위터에 등록된 photolog 어플리케이션 인증키 (https://dev.twitter.com/)
APP_KEY    = 'tha1vwfKSJ0jlDcdCryvag'
APP_SECRET = '84qXU6uv1XyDbM780civoBA7U4mnmKEQ0FnaBQn63go'


@photolog.route('/sns/twitter/send/<photolog_id>')
def send(photolog_id):
    """ photolog_id에 해당하는 사진과 커멘트를 트위터로 전송하는 함수 """

    if (session.__contains__('TWITTER')):
        twitter = session['TWITTER']
        # 파라미터로 받은 photolog_id를 이용하여 해당 사진과 커멘트를 트위터로 전송한다.
        photo = open(photo_realpath(photolog_id), 'rb')
        twitter.update_status_with_media(status=photo_comment(photolog_id), media=photo)

        return redirect(url_for('.show_all'))

    else:
        # twitter 객체가 세션에 없을경우 인증단계로 이동한다.
        return redirect(url_for('.oauth', photolog_id=photolog_id))



@photolog.route('/sns/twitter/oauth/<photolog_id>')
def oauth(photolog_id):
    """ twitter로부터 인증토큰을 받기 위한 함수 """
    
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens(callback_url='http://photolog.codingstar.net:5000/sns/twitter/callback/'+photolog_id)
    
    # 중간단계로 받은 임시 인증토큰은 최종인증을 위해 필요하므로 세션에 저장한다. 
    session['OAUTH_TOKEN'] = auth['oauth_token']
    session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

    # 트위터의 사용자 권한 인증 URL로 페이지를 리다이렉트한다.
    return redirect(auth['auth_url'])




@photolog.route('/sns/twitter/callback/<photolog_id>')
def callback(photolog_id):
    """ twitter로부터 callback url이 요청되었을때 
        최종인증을 한 후 트위터로 해당 사진과 커멘트를 전송한다.  
    """

    Log.info("callback oauth_token:" + request.args['oauth_token']);
    Log.info("callback oauth_verifier:" + request.args['oauth_verifier']);
    
    # oauth에서 twiter로 부터 넘겨받은 인증토큰을 세션으로 부터 가져온다.
    OAUTH_TOKEN        = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    oauth_verifier     = request.args['oauth_verifier']
    
    # 임시로 받은 인증토큰을 이용하여 twitter 객체를 만들고 인증토큰을 검증한다.     
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    final_step = twitter.get_authorized_tokens(oauth_verifier)    
    
    # oauth_verifier를 통해 얻은 최종 인증토큰을 이용하여 twitter 객체를 새로 생성한다.
    twitter = Twython(APP_KEY, APP_SECRET, final_step['oauth_token'], final_step['oauth_token_secret'])
    session['TWITTER'] = twitter

    # 파라미터로 받은 photolog_id를 이용하여 해당 사진과 커멘트를 트위터로 전송한다.
    photo = open(photo_realpath(photolog_id), 'rb')
    twitter.update_status_with_media(status=photo_comment(photolog_id), media=photo)

    return redirect(url_for('.show_all'))

