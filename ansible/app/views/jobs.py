# -*- coding: utf8 -*-

import os
import ast
import time
import glob
import codecs
from collections import defaultdict
from passlib.hash import sha512_crypt
import pickle
from amqplib import client_0_8 as amqp
from flask import Blueprint, g, render_template, request, redirect, url_for

from app import app
from app import permision
from app.forms.jobs import AddGeneralJobForm
from app.forms.jobs import JobAddUserForm
from app.forms.jobs import JobDelUserForm
from app.forms.jobs import JobAddUserByPubkeyForm
from app.forms.jobs import ReActionForm
from app.forms.jobs import JobMysqlForm
from app.forms.jobs import JobPhpForm


blueprint = Blueprint('jobs', __name__)


def send2amqp(yml_temp_name, args):
    started = str(int(time.time()))
    g.mysql_db.execute("INSERT INTO jobs(started, template_name, args) \
            VALUES(%s, %s, %s)", started, yml_temp_name, pickle.dumps(args))

    body = (started, yml_temp_name, args)
    msg = amqp.Message(pickle.dumps(body))
    msg.properties['delivery_mode'] = 2    #持久化消息
    g.amqp_chan.basic_publish(msg, exchange="sorting_room", routing_key="json")


def get_alias():
    hosts = g.mysql_db.query('select A.id,alias,ip,port,remote_user, \
            name as group_name from \
            (select hosts.id,alias,ip,port,remote_user,group_id from hosts \
            left join host_group on hosts.id=host_group.host_id) A \
            left join groups on A.group_id=groups.id')
    r = defaultdict(list)
    for host in hosts:
        r[host.get('group_name')].append(host)
    results = []
    for i in r:
        results.append(("{}".format(i),"*{}".format(i)))
        for j in r.get(i):
            results.append((j.get('alias'),j.get('alias')))
    return results


@blueprint.route('/', methods=['GET', 'POST'])
@permision
def index():
    form = ReActionForm()
    if form.validate_on_submit():
        yml_temp_name = form.yml_temp_name.data
        args = ast.literal_eval(form.argss.data)
        send2amqp(yml_temp_name, args)
        return redirect(url_for('jobs.index'))
    jobs = g.mysql_db.query("SELECT * FROM jobs LIMIT 1000")
    return render_template('jobs.html', jobs=jobs, form=form)


@blueprint.route('/add_general', methods=['GET', 'POST'])
@permision
def add_general():
    form = AddGeneralJobForm()
    form.yml_temp_name.choices = [(i, i) for i in os.listdir(app.config['YML_TEMP_PATH']) if i[0] != '_']
    form.selected_alias.choices = get_alias()
    if form.validate_on_submit():
        host = ':'.join(form.selected_alias.data)
        user = form.remote_user.data
        yml_temp_name = form.yml_temp_name.data
        args = {'host': host,
                'user': user}
        send2amqp(yml_temp_name, args)
        return redirect(url_for("jobs.index"))

    return render_template('add_general_job.html', form=form)


@blueprint.route('/add_other', methods=['GET', 'POST'])
@permision
def add_other():
    return render_template('add_other_job.html')


@blueprint.route('/add_user', methods=['GET', 'POST'])
@permision
def add_user():
    form = JobAddUserForm()
    form.selected_alias.choices = get_alias()
    if form.validate_on_submit():
        host = ':'.join(form.selected_alias.data)
        user = form.remote_user.data
        username = form.username.data
        password = form.password.data
        passwd_sha512 = sha512_crypt.encrypt(password)
        yml_temp_name = form.yml_temp_name.data
        args = {'host': host,
                'user': user,
                'username': username,
                'password': passwd_sha512
                }
        send2amqp(yml_temp_name, args)
        return redirect(url_for("jobs.index"))
    
    yml_temp_name = '_add_user'
    return render_template('job_add_user.html',form=form,
            yml_temp_name=yml_temp_name)


@blueprint.route('/del_user', methods=['GET', 'POST'])
@permision
def del_user():
    form = JobDelUserForm()
    form.selected_alias.choices = get_alias()
    if form.validate_on_submit():
        host = ':'.join(form.selected_alias.data)
        user = form.remote_user.data
        username = form.username.data
        if username == u'root':
            username = u'test'
        yml_temp_name = form.yml_temp_name.data
        args = {'host': host,
                'user': user,
                'username': username
                }
        send2amqp(yml_temp_name, args)
        return redirect(url_for("jobs.index"))
    
    yml_temp_name = '_del_user'
    return render_template('job_del_user.html',form=form,
            yml_temp_name=yml_temp_name)


@blueprint.route('/add_user_by_pubkey', methods=['GET', 'POST'])
@permision
def add_user_by_pubkey():
    form = JobAddUserByPubkeyForm()
    form.selected_alias.choices = get_alias()
    form.key.choices = [(os.path.basename(i), os.path.basename(i)) for i in glob.glob(os.path.join(app.config['KEYDIR'], '*.pub'))]
    if form.validate_on_submit():
        host = ':'.join(form.selected_alias.data)
        user = form.remote_user.data
        username = form.username.data
        key = form.key.data
        key = codecs.open(os.path.join(app.config['KEYDIR'], key), 'r').read()
        yml_temp_name = form.yml_temp_name.data
        args = {'host': host,
                'user': user,
                'username': username,
                'key': key
                }
        send2amqp(yml_temp_name, args)
        return redirect(url_for("jobs.index"))
    
    yml_temp_name = '_add_user_by_pubkey'
    return render_template('job_add_user_by_pubkey.html',form=form,
            yml_temp_name=yml_temp_name)


@blueprint.route('/mysql', methods=['GET', 'POST'])
@permision
def mysql():
    form = JobMysqlForm()
    form.selected_alias.choices = get_alias()
    if form.validate_on_submit():
        host = ':'.join(form.selected_alias.data)
        user = form.remote_user.data
        mysql_data_dir = form.mysql_data_dir.data
        yml_temp_name = form.yml_temp_name.data
        args = {'host': host,
                'user': user,
                'mysql_data_dir': mysql_data_dir
                }
        send2amqp(yml_temp_name, args)
        return redirect(url_for("jobs.index"))
    
    yml_temp_name = '_mysql5.5'
    return render_template('job_mysql5.5.html',form=form,
            yml_temp_name=yml_temp_name)


@blueprint.route('/php', methods=['GET', 'POST'])
@permision
def php():
    form = JobPhpForm()
    form.selected_alias.choices = get_alias()
    if form.validate_on_submit():
        host = ':'.join(form.selected_alias.data)
        user = form.remote_user.data
        mysql_data_dir = form.mysql_data_dir.data
        yml_temp_name = form.yml_temp_name.data
        args = {'host': host,
                'user': user,
                'mysql_data_dir': mysql_data_dir
                }
        send2amqp(yml_temp_name, args)
        return redirect(url_for("jobs.index"))
    
    yml_temp_name = '_php5.3'
    return render_template('job_php5.3.html',form=form,
            yml_temp_name=yml_temp_name)


@blueprint.route('/jobs_log', methods=['GET', 'POST'])
@permision
def log():
    log = codecs.open(app.config['ANSIBLE_LOG'], encoding='utf-8')
    return render_template('jobs_log.html', logs=log.readlines())


@blueprint.route('/amqp_log', methods=['GET', 'POST'])
@permision
def amqp_log():
    log = codecs.open(app.config['AMQP_LOG'], encoding='utf-8')
    return render_template('amqp_log.html', logs=log.readlines())

