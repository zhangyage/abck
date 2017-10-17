# -*- coding: utf8 -*-

import re
import torndb
from functools import wraps
from amqplib import client_0_8 as amqp
from flask import Flask, g, current_app, request, redirect, url_for
from flask.ext.login import LoginManager, UserMixin, login_user, current_user, \
        logout_user, login_required
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)


@app.before_request
def connect_db():
    g.mysql_db = torndb.Connection(host=app.config['DB_HOST'],
                             user=app.config['DB_USER'],
                             password=app.config['DB_PASS'],
                             database=app.config['DB_NAME'],
                             charset='utf8'
                             )
    g.amqp_db = amqp.Connection(host=app.config['AMQP_HOST'],
                                userid=app.config['AMQP_USERID'],
                                password=app.config['AMQP_PASSWORD'],
                                virtual_host='/',
                                insist=False
                                )
    g.amqp_chan = g.amqp_db.channel()


@app.teardown_request
def close_connection(response):
    g.mysql_db.close()
    g.amqp_chan.close()
    g.amqp_db.close()
    return response


# flask-bcrypt
bcrypt = Bcrypt(app)


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'users.login'


class User(UserMixin):
    def __init__(self, userdict):
        self.id = userdict.get('id')
        self.username = userdict.get('username')
        self.password = userdict.get('password')
        self.active = userdict.get('active')

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.active == 1:
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


@login_manager.user_loader
def load_user(userid):
    user = g.mysql_db.get("select * from users where id=%s", userid)
    return User(user)


def uri_match(re_str, uri):
    # re_str: /users/*
    # uri: /users/login, /users/logout
    if re.match(re_str, uri):
        return True
    else:
        return False


def permision(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        results = g.mysql_db.get("select group_concat(path) as re_strs from \
                (select * from users left join (select user_id,user_role.role_id, \
                route_id from user_role inner join role_route on \
                user_role.role_id=role_route.role_id) A on \
                users.id=A.user_id) B left join routes on B.route_id= routes.id \
                where username=%s", current_user.username)
        uri = unicode(request.url_rule)
        re_strs = results.get('re_strs')
        if re_strs:
            match = False
            for re_str in re_strs.split(','):
                match = uri_match(re_str, uri)
                if match:
                    break
            if match:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('errors.forbidden'))
        else:
            return redirect(url_for('errors.forbidden'))
    return decorated_view


# Views
from views import *

