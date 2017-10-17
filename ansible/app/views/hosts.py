# -*- coding: utf8 -*-

import pickle
import ast
import time
from flask import Blueprint, g, render_template, request, redirect, url_for
from ansible.runner import Runner

from app import app
from app import utils as autils
from app import permision
from app.forms.hosts import AddHostForm, EditHostForm
from app.forms.hosts import AddSSHKeyForm


blueprint = Blueprint("hosts", __name__)


@blueprint.route('/')
@permision
def index():
    hosts = g.mysql_db.query("SELECT * from hosts")
    return render_template('hosts.html', hosts=hosts)


def get_alias_info(pattern,remote_user):
    runner = Runner(
            module_name='setup',
            module_args='',
            pattern=pattern,
            inventory=autils.get_inventory(g.mysql_db),
            remote_user=remote_user)
    info = runner.run()

    results = {}

    if info['contacted']:
        if not info['contacted'][pattern].has_key('failed'):
            facts = info['contacted'][pattern]['ansible_facts']
            # Server info
            results['system_vendor'] = facts['ansible_system_vendor']
            results['product_name'] = facts['ansible_product_name']
            results['product_serial'] = facts['ansible_product_serial']
            # System info
            results['distribution'] = facts['ansible_distribution']
            results['distribution_version'] = facts['ansible_distribution_version']
            results['architecture'] = facts['ansible_architecture']
            results['kernel'] = facts['ansible_kernel']
            # Cpu info 
            results['processor_count'] = facts['ansible_processor_count']
            results['processor_cores'] = facts['ansible_processor_cores']
            results['processor_vcpus'] = facts['ansible_processor_vcpus']
            results['processor_threads_per_core'] = facts['ansible_processor_threads_per_core']
            results['processor'] = set(facts['ansible_processor'])
            # Swap info
            results['swaptotal_mb'] = facts['ansible_swaptotal_mb']
            results['swapfree_mb'] = facts['ansible_swapfree_mb']
            # Mem info
            results['memtotal_mb'] = facts['ansible_memtotal_mb']
            results['memfree_mb'] = facts['ansible_memfree_mb']
            # Disk info
            results['devices'] = facts['ansible_devices']
            # Mount info
            results['mounts'] = facts['ansible_mounts']
            # Ip info
            results['default_ipv4'] = facts['ansible_default_ipv4']
            results['all_ipv4_addresses'] = facts['ansible_all_ipv4_addresses']
            # Software 
            results['selinux'] = facts['ansible_selinux']
            results['python_version'] = facts['ansible_python_version']
        else:
            facts = info['contacted'][pattern]
            results['failed'] = facts['failed']
            results['msg'] = facts['msg']
    elif info['dark']:
        facts = info['dark'][pattern] 
        results['failed'] = facts['failed']
        results['msg'] = facts['msg']
    else:
        results['failed'] = False
        results['msg'] = "host not found"

    return results


@blueprint.route('/host/<alias>/', methods=['GET', 'POST'])
@permision
def show_alias(alias):
    alias_info = g.mysql_db.get("SELECT * FROM hosts LEFT JOIN host_info \
            ON hosts.id=host_info.host_id WHERE alias=%s", alias)
    if request.method == 'POST':
        info = get_alias_info(alias_info.get('alias'), alias_info.get('remote_user'))
        last_update = time.time()
        info['host_id'] = alias_info.get('id')
        info['last_update'] = last_update
        if info.get('failed'):
            g.mysql_db.execute("REPLACE INTO host_info (host_id, last_update, failed, msg) \
                    VALUES (%s, %s, %s, %s)", info['host_id'], info['last_update'], 
                    info['failed'], info['msg'])
        else:
            cloums = ' ,'.join(['"%s"'] * len(info.keys()))
            sql = "REPLACE INTO host_info (%s) VALUES (%s)" % (' ,'.join(info.keys()), cloums)
            g.mysql_db.execute(sql % tuple(info.values()))
        return redirect(url_for('.show_alias', alias=alias))
    return render_template('show_alias.html', alias_info=alias_info)


@blueprint.route('/add', methods=['GET', 'POST'])
@permision
def add():
    form = AddHostForm()
    if form.validate_on_submit():
        alias = form.alias.data
        ip = form.ip.data
        ip2 = form.ip2.data
        port = form.port.data
        remote_user = form.remote_user.data
        if ip2:
            g.mysql_db.execute("INSERT INTO hosts(alias, ip, ip2, port, remote_user) \
                    VALUES(%s,%s,%s,%s,%s)", alias, ip, ip2, port, remote_user)
        else:
            g.mysql_db.execute("INSERT INTO hosts(alias, ip, port, remote_user) \
                    VALUES(%s,%s,%s,%s)", alias, ip, port, remote_user)
        return redirect(url_for('.index'))
    return render_template('add_host.html', form=form)


@blueprint.route('/host/<alias>/edit', methods=['GET', 'POST'])
@permision
def edit_host(alias):
    form = EditHostForm()
    if form.validate_on_submit():
        ip = form.ip.data
        ip2 = form.ip2.data
        port = form.port.data
        remote_user = form.remote_user.data
        if ip2 and ip2 != u'None':
            g.mysql_db.execute("UPDATE hosts SET ip=%s, ip2=%s, port=%s, remote_user=%s \
                    WHERE alias=%s", ip, ip2, port, remote_user, alias)
        else:
            g.mysql_db.execute("UPDATE hosts SET ip=%s, port=%s, remote_user=%s \
                    WHERE alias=%s", ip, port, remote_user, alias)
        return redirect(url_for('.index'))
    host = g.mysql_db.get('SELECT * FROM hosts WHERE alias=%s', alias)
    return render_template('edit_host.html', host=host, form=form)


@blueprint.route('/host/<alias>/add_sshkey', methods=['GET', 'POST'])
@permision
def add_sshkey(alias):
    form = AddSSHKeyForm()
    if form.validate_on_submit():
        remote_user = form.remote_user.data
        remote_pass = form.remote_pass.data

        runner = Runner(
                module_name='authorized_key',
                module_args={'user': remote_user,
                             'key': open(app.config['ANSIBLE_KEY']).read()
                             },
                pattern=alias,
                inventory=autils.get_inventory(g.mysql_db),
                remote_user=remote_user,
                remote_pass=remote_pass)
        info = runner.run()
        return redirect(url_for('.index'))

    host = g.mysql_db.get('SELECT * FROM hosts WHERE alias=%s', alias)
    return render_template('add_sshkey.html', host=host, form=form)
