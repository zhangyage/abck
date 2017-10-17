# -*- coding: utf8 -*-

from flask import Blueprint, g, render_template, redirect, url_for
from app.forms.groups import AddGroupForm, EditGroupForm
from collections import defaultdict

from app import permision

blueprint = Blueprint('groups', __name__)


@blueprint.route('/')
@permision
def index():
    groups = g.mysql_db.query("select group_name,group_id,description,group_concat(alias) \
            as members from (select host_id,id as group_id,alias,name as \
            group_name,description from groups left join (select host_id,group_id, alias \
            from host_group inner join hosts on host_group.host_id=hosts.id) A \
            on groups.id=A.group_id) aa group by group_id")
    return render_template('groups.html', groups=groups)


@blueprint.route('/add', methods=['GET', 'POST'])
@permision
def add():
    form = AddGroupForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        if description:
            g.mysql_db.execute("INSERT INTO groups(name, description) \
                    VALUES(%s, %s)", name, description)
        else:
            g.mysql_db.execute("INSERT INTO groups(name) \
                    VALUES(%s)", name)

        return redirect(url_for('.index'))
    return render_template('add_group.html', form=form)


def get_all_alias():
    hosts = g.mysql_db.query('select id,alias, count(distinct alias) from \
            hosts group by alias')
    results = []
    for host in hosts:
        results.append((unicode(host.get('id')),host.get('alias')))
    return results


def get_members_by_group(group):
    members_d = g.mysql_db.get("select group_name,group_id, \
            group_concat(alias) as members,group_concat(host_id) \
            as members_id from (select host_id,id \
            as group_id,alias,name as group_name from groups \
            left join (select host_id,group_id, alias from \
            host_group inner join hosts on host_group.host_id=hosts.id) A \
            on groups.id=A.group_id) aa where group_name=%s", group)
    if members_d.get('members'):
        return (members_d.get('group_id'),
                members_d.get('members').split(','),
                members_d.get('members_id').split(','))
    else:
        return (members_d.get('group_id'), [],[])


@blueprint.route('/<group>/edit', methods=['GET', 'POST'])
@permision
def edit(group):
    form = EditGroupForm()
    form.selected_members.choices = get_all_alias()
    group_id, cur_members, cur_members_id = get_members_by_group(group)
    gp = g.mysql_db.get("select * from groups where name=%s", group)
    if form.validate_on_submit():
        new_members_id = form.selected_members.data
        description = form.description.data
        if description:
            g.mysql_db.execute("update groups set description=%s where name=%s",
                    description, group)

        del_members_id = list(set(cur_members_id) - set(new_members_id))
        ins_members_id = list(set(new_members_id) - set(cur_members_id))
        if del_members_id:
            g.mysql_db.executemany("delete from host_group where group_id=%s \
                    and host_id=%s", [(group_id, i) for i in del_members_id])
        if ins_members_id:
            g.mysql_db.executemany("insert into host_group(group_id,host_id) \
                    value(%s, %s)", [(group_id, i) for i in ins_members_id])
        return redirect(url_for('.index'))
    return render_template('edit_group.html', group=group, cur_members=cur_members,
            form=form, gp=gp)
