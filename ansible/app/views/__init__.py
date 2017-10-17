# -*- coding: utf8 -*-

import pickle
import time

from app import app


# Blueprint
import admin, hosts, jobs, groups, users, errors

app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(hosts.blueprint, url_prefix='/hosts')
app.register_blueprint(groups.blueprint, url_prefix='/groups')
app.register_blueprint(jobs.blueprint, url_prefix='/jobs')
app.register_blueprint(users.blueprint, url_prefix='/users')
app.register_blueprint(errors.blueprint, url_prefix='/errors')


def pickle_loads(value):
    if value:
        return pickle.loads(value)
    else:
        return value


def _eval(value):
    if value:
        return eval(value)
    else:
        return value


def job_unreachable(value):
    i = 0
    for j in value:
        if value.get(j)['unreachable']:
            i = i + value.get(j)['unreachable']
    return i

def job_failed(value):
    i = 0
    for j in value:
        if value.get(j)['failures']:
            i = i + value.get(j)['failures']
    return i


def format_datetime(value):
    if value:
        sec = int(value)
        t = time.localtime(sec)
        return "%04i-%02i-%02i %02i:%02i:%02i" % (t.tm_year, t.tm_mon, t.tm_mday,
            t.tm_hour, t.tm_min, t.tm_sec)
    else:
        return None


def format_split(value):
    return value.split(',')


app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['pickle_loads'] =  pickle_loads
app.jinja_env.filters['eval'] =  _eval
app.jinja_env.filters['job_unreachable'] =  job_unreachable
app.jinja_env.filters['job_failed'] =  job_failed
app.jinja_env.filters['split'] =  format_split
