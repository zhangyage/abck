# -*- coding: utf8 -*-

from flask import g
from flask.ext.wtf import Form
from wtforms import fields, validators


class AddHostForm(Form):
    alias = fields.TextField('Alias', [validators.InputRequired()])
    ip = fields.TextField('Ip', [validators.IPAddress()])
    ip2 = fields.TextField('Ip2')
    port = fields.IntegerField('Port', [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])

    def validate_alias(form, field):
        results = [i.get('alias') for i in  g.mysql_db.query('SELECT alias FROM hosts') if i]
        if field.data in results:
            raise validators.ValidationError("{} is exists!".format(field.data))

class EditHostForm(Form):
    alias = fields.TextField('Alias', [validators.InputRequired()])
    ip = fields.TextField('Ip', [validators.IPAddress()])
    ip2 = fields.TextField('Ip2')
    port = fields.IntegerField('Port', [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])


class AddSSHKeyForm(Form):
    alias = fields.TextField('Alias', [validators.InputRequired()])
    remote_user = fields.TextField('Remote User', [validators.InputRequired()])
    remote_pass = fields.PasswordField('Remote Password', [validators.InputRequired()])
