# -*- coding: utf8 -*-

from flask import Blueprint, render_template

from app import permision


blueprint = Blueprint('errors', __name__)


@blueprint.route('/forbidden')
def forbidden():
    return render_template('forbidden.html')
