# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user

from app import User, bcrypt
from app import permision
from app.forms.users import LoginForm, ChangedPasswordForm


blueprint = Blueprint('users', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(User(user))
        return form.redirect(url_for('admin.index'))
    return render_template('login.html', form=form)


@blueprint.route('/logout')
@permision
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@blueprint.route('/<username>/profile', methods=['GET', 'POST'])
@permision
def profile(username):
    form = ChangedPasswordForm()
    if form.validate_on_submit():
        user_name = form.username.data
        if username != user_name:
            abort(404)
        new_password = form.new_password.data
        g.mysql_db.execute('UPDATE users SET password=%s WHERE username=%s',
                bcrypt.generate_password_hash(new_password), user_name)
        return redirect(url_for('admin.index'))
    return render_template('profile.html', form=form)
