# -*- coding: utf8 -*-

from flask import Blueprint, render_template
from flask.ext.login import current_user

from app import permision

blueprint = Blueprint('admin', __name__)


@blueprint.route('/')
@permision
def index():
    return render_template('admin.html', current_user=current_user)
