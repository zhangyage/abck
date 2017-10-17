# -*- coding: utf8 -*-

import os
import time
import json
import codecs


_basedir = os.path.abspath(os.path.dirname(__file__))

log_path = os.path.join(_basedir, '../../logs/jobs.log')
TIME_FORMAT="%b %d %Y %H:%M:%S"
#FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout', 'stderr']
FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stderr']


def log(host, category, data):
    if type(data) == type(dict()):
        for field in FIELDS:
            if field in data.keys():
                data = data.copy()
                encoded_field = unicode(data[field])

                now = time.strftime(TIME_FORMAT, time.localtime())
                fd = codecs.open(log_path, "a", encoding='utf-8')
                fd.write('{now} - {host} - {category} - {field}:{encoded_field}\n'.format(now=now, 
                    host=host, 
                    category=category, 
                    field=field, 
                    encoded_field=encoded_field))
                fd.close()

def log_msg(msg):
    now = time.strftime(TIME_FORMAT, time.localtime())
    fd = open(log_path, "a")
    fd.write(msg)
    fd.close()


class CallbackModule(object):
    
    
    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        log(host, 'FAILED', res)

    def runner_on_ok(self, host, res):
        log(host, 'OK', res)

    def runner_on_skipped(self, host, item=None):
        log(host, 'SKIPPED', '...')

    def runner_on_unreachable(self, host, res):
        log(host, 'UNREACHABLE', res)

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        log(host, 'ASYNC_POLL', res)

    def runner_on_async_ok(self, host, res, jid):
        log(host, 'ASYNC_OK', res)

    def runner_on_async_failed(self, host, res, jid):
        log(host, 'ASYNC_FAILED', res)

    def playbook_on_start(self):
        log_msg("*" * 79 + '\n')

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None,
            encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        log(host, 'IMPORTED', imported_file)
    
    def playbook_on_not_import_for_host(self, host, missing_file):
        log(host, 'NOTIMPORTED', missing_file)

    def playbook_on_play_start(self, name):
        pass

    def playbook_on_stats(self, stats):
        pass


