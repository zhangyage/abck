# -*- coding: utf8 -*-

import os


_basedir = os.path.abspath(os.path.dirname(__file__))


# YML Template path
YML_TEMP_PATH = os.path.join(_basedir, 'app/yml_temp')

# Ansible Key
ANSIBLE_KEY = '/root/.ssh/id_rsa.pub'

# Key dir
KEYDIR = os.path.join(_basedir, 'app/keydir')

# key
SECRET_KEY = os.urandom(24)

# RBAC
RBAC_USE_WHITE = True

# Debug
DEBUG = True

# DB
DB_HOST = "127.0.0.1"
DB_PORT= 3306
DB_USER = "root"
DB_PASS = ""
DB_NAME = "ansible"

# AMQP
AMQP_HOST = 'localhost'
AMQP_USERID = 'guest'
AMQP_PASSWORD = 'guest'

# LOG
ANSIBLE_LOG = os.path.join(_basedir, 'app/logs/jobs.log')
AMQP_LOG = os.path.join(_basedir, 'app/logs/amqp.log')
AMQP_LOG_FORMATTER = "[%(asctime)s] %(levelname)s - %(message)s"


del os
