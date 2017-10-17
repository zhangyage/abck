# -*- coding: utf8 -*-

import os
import sys
import time
import torndb
import pickle
import traceback
import logging
from logging import handlers
from daemon import Daemon
from amqplib import client_0_8 as amqp
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
from app import app
from app import utils as autils


handler = handlers.TimedRotatingFileHandler(app.config['AMQP_LOG'],
                                            when='midnight',
                                            interval=1,
                                            backupCount=0)
formatter = logging.Formatter(app.config['AMQP_LOG_FORMATTER'])
handler.setFormatter(formatter)

logger = logging.getLogger('amqp')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def ansible_book(db, pb, args):
    playbook_cp = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    playbook = PlayBook(playbook=pb,
                        extra_vars=args,
                        callbacks=playbook_cp,
                        stats=stats,
                        runner_callbacks=runner_cb,
                        inventory=autils.get_inventory(db)
                        )

    try:
        results = playbook.run()
    except:
        logger.error(traceback.format_exc())
        results = {'error': {'unreachable': 0, 'skipped': 0, 'ok': 0, 'changed': 0, 'failures': 1}}
    return results


def recv_callback(msg):
    db = torndb.Connection(host=app.config['DB_HOST'],
                             user=app.config['DB_USER'],
                             password=app.config['DB_PASS'],
                             database=app.config['DB_NAME'],
                             charset='utf8'
                             )

    started, yml_temp_name, args = pickle.loads(msg.body)
    logger.info("started: %s" % started)
    logger.info("yml_temp_name: %s" % yml_temp_name)
    logger.info("args: %s" % args)
    pb = os.path.join(os.path.join(app.config['YML_TEMP_PATH'], yml_temp_name), 'main.yml')
    status = ansible_book(db, pb, args)
    finished = str(int(time.time()))
    #db.update_jobs((str(pickle.dumps(status)), finished, started))
    upd_jobs_sql = 'UPDATE jobs SET status=%s, finished=%s where started=%s'
    db.execute(upd_jobs_sql, pickle.dumps(status), finished, started)
    logger.info("status: %s" % status)


class AmqpConsumerDaemon(Daemon):
    def run(self):
        conn = amqp.Connection(host=app.config['AMQP_HOST'],
                       userid=app.config['AMQP_USERID'],
                       password=app.config['AMQP_PASSWORD'],
                       virtual_host='/',
                       insist=False)
        chan = conn.channel()
        chan.queue_declare(queue="po_box", durable=True, exclusive=False, auto_delete=False)
        chan.exchange_declare(exchange="sorting_room", type="direct", durable=True, auto_delete=False)
        chan.queue_bind(queue="po_box", exchange="sorting_room", routing_key="json")

        chan.basic_consume(queue="po_box", no_ack=True, callback=recv_callback, consumer_tag="testtag")

        while True:
            try:
                chan.wait()
            except:
                logger.error(traceback.format_exc())

        chan.basic_cancel("testtag")

        chan.close()
        conn.close()


if __name__ == "__main__":
    daemon = AmqpConsumerDaemon('/tmp/amqp_consumer.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
