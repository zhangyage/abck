# -*- coding: utf8 -*-

from flask import g
from flask.ext.wtf import Form
from wtforms import fields, validators


class ReActionForm(Form):
    yml_temp_name = fields.TextField('Template Name', [validators.InputRequired()])
    argss = fields.TextField('Args', [validators.InputRequired()])


class AddGeneralJobForm(Form):
    yml_temp_name = fields.SelectField('Template Name', [validators.InputRequired()])
    selected_alias = fields.SelectMultipleField('Select Group / Host',
            [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])


class JobAddUserForm(Form):
    yml_temp_name = fields.TextField('Template Name', [validators.InputRequired()])
    selected_alias = fields.SelectMultipleField('Select Group / Host',
            [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])
    username = fields.TextField('Username', [validators.InputRequired()])
    password = fields.PasswordField('Password', [validators.InputRequired()])


class JobDelUserForm(Form):
    yml_temp_name = fields.TextField('Template Name', [validators.InputRequired()])
    selected_alias = fields.SelectMultipleField('Select Group / Host',
            [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])
    username = fields.TextField('Username', [validators.InputRequired()])


class JobAddUserByPubkeyForm(Form):
    yml_temp_name = fields.TextField('Template Name', [validators.InputRequired()])
    selected_alias = fields.SelectMultipleField('Select Group / Host',
            [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])
    username = fields.TextField('Username', [validators.InputRequired()])
    #key = fields.TextAreaField('Key', [validators.InputRequired()])
    key = fields.SelectField('Key', [validators.InputRequired()])

class JobMysqlForm(Form):
    yml_temp_name = fields.TextField('Template Name', [validators.InputRequired()])
    selected_alias = fields.SelectMultipleField('Select Group / Host',
            [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])
    mysql_data_dir = fields.TextField('MySQL Data Dir', [validators.InputRequired()])

class JobPhpForm(Form):
    yml_temp_name = fields.TextField('Template Name', [validators.InputRequired()])
    selected_alias = fields.SelectMultipleField('Select Group / Host',
            [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])
    mysql_data_dir = fields.TextField('MySQL Data Dir', [validators.InputRequired()])
