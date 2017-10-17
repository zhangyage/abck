# -*- coding: utf8 -*-

from flask import g
from flask.ext.wtf import Form
from wtforms import fields, validators


class AddGroupForm(Form):
    name = fields.TextField('Name', [validators.InputRequired()])

    def validate_name(form, field):
        results = [i.get('name') for i in g.mysql_db.query('SELECT name FROM groups') if i]
        if field.data in results:
            raise validators.ValidationError("{} is exists!".format(field.data))

    description = fields.TextField('Description')


class EditGroupForm(Form):
    name = fields.TextField('Name', [validators.InputRequired()])
    description = fields.TextField('Description')
    selected_members = fields.SelectMultipleField('Members')

