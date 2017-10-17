# -*- coding: utf8 -*-

import os
import torndb
from tempfile import NamedTemporaryFile

#import ansible
from ansible.inventory import Inventory
#from ansible.runner import Runner

from collections import defaultdict
import ansible.runner
import ansible.playbook
from ansible import callbacks
from ansible import utils


class Ansible_Handler:
    def __init__(self,host=None,port=None,name=None,groups=None):
        self._hosts=[]
        self.add_host(host,port,name,groups)

    def add_host(self,host,port=None,name=None,groups=None):
        if not host == None:
            host=str(host)

        if not name == None:
            name=str(name)

        if not port == None:
            port = int(port)

        if groups == None:
            groups = []

        tmp_grp=[]
        for group in groups:
            tmp_grp.append(str(group))

        if host == None and name == None and port == None and groups == []:
            pass
        else:
            self._hosts.append((name,host,port,groups))
            self._inventory = None

    @property
    def default_group(self):
        return 'default'

    @property
    def default_name(self):
        return self.default_group

    @property
    def hosts(self):
        return self._hosts

    @property
    def groups(self):
        unique_groups=[]
        for host in self.hosts:
            _, _, _, groups = host
            if groups == None or groups == []:
                groups = [self.default_group]
            for group in groups:
                if group not in unique_groups:
                    unique_groups.append(group)
        return unique_groups

    @property
    def inventory_string(self):
       names_and_groups=[]
       inventory_string=[]

       string=''
       i=0

       incrementer=0
       incrementer_minlength=3


       for item in self.hosts:
           name, host, port, groups = item
           if name == None:
               default_append=""
               if incrementer > 0:
                   default_append=incrementer
                   while len(str(default_append)) < incrementer_minlength:
                       default_append='0%s'%default_append
               if default_append == "":
                   name="%s"%self.default_name
               else:
                   name="%s_%s"%(self.default_name,default_append)
           incrementer+=1

           if host == 'localhost':
               line="%s %s"%(name, host)
           else:
               line="%s ansible_ssh_host=%s"%(name,host)

           if not port == None:
               line="%s ansible_ssh_port=%s"%(line,port)

           inventory_string.append(line)
           names_and_groups.append((name,groups))

       for group in self.groups:
           inventory_string.append('')
           inventory_string.append('[%s]'%(group,))

           for name, groups in names_and_groups:
               if groups == []:
                   groups = [self.default_group]
               if group in groups:
                   inventory_string.append(name)


       return "\n".join(inventory_string)

    @property
    def inventory(self):
        if self._inventory == None:
            tmpfile = NamedTemporaryFile()
            try:
                tmpfile.write(self.inventory_string)
                tmpfile.seek(0)
                self._inventory = Inventory(tmpfile.name)
            finally:
                tmpfile.close()
        return self._inventory

    def run_playbook(self,playbook_path):
        if not os.path.isfile(playbook_path):
            raise CONF_NotaFile("Can't run ansible playbook, not a file: %s"%playbook_path)

        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

        pb = ansible.playbook.PlayBook(
            playbook=playbook_path,
            stats=stats,
            callbacks=playbook_cb,
            runner_callbacks=runner_cb,
            check=True,
            inventory = self.inventory
        )

        pb.run()


def get_inventory(db):
    #hosts = db.select_inventory()
    sel_inv_sql = 'select A.id,alias,ip,port,remote_user,name as group_name from \
        (select hosts.id,alias,ip,port,remote_user,group_id from hosts \
        left join host_group on hosts.id=host_group.host_id) A \
        left join groups on A.group_id=groups.id'
    hosts = db.query(sel_inv_sql)
    handler = Ansible_Handler()
    results = defaultdict(list)
    if hosts is not None:
        for host in hosts:
            results[host.get('alias')].append(host)

        for _, result in results.iteritems():
            handler.add_host(name=result[0].get('alias'),
                             host=result[0].get('ip'),
                             port=result[0].get('port'),
                             groups=[i.get('group_name') for i in result]
                             )

    return handler.inventory


if __name__ == '__main__':
    db = torndb.Connection(host=app.config['DB_HOST'],
                             user=app.config['DB_USER'],
                             password=app.config['DB_PASS'],
                             database=app.config['DB_NAME'],
                             charset='utf8'
                             )
    sel_inv_sql = 'select A.id,alias,ip,port,remote_user,name as group_name from \
        (select hosts.id,alias,ip,port,remote_user,group_id from hosts \
        left join host_group on hosts.id=host_group.host_id) A \
        left join groups on A.group_id=groups.id'
    hosts = db.query(sel_inv_sql)
    handler = Ansible_Handler()
    results = defaultdict(list)
    if hosts is not None:
        for host in hosts:
            results[host.get('alias')].append(host)

        for _, result in results.iteritems():
            handler.add_host(name=result[0].get('alias'),
                             host=result[0].get('ip'),
                             port=result[0].get('port'),
                             groups=[i.get('group_name') for i in result]
                             )

    
    print handler.inventory_string
