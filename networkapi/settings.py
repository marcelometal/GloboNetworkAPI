# -*- coding:utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import logging

reload(sys)

sys.setdefaultencoding('utf-8')

# Include base path in system path for Python old.
syspath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if not syspath in sys.path:
    sys.path.insert(0, syspath)

def LOCAL_FILES(path):
    new_path = os.path.abspath(os.path.join(__file__, path))
    return new_path

NETWORKAPI_USE_NEWRELIC = os.getenv('NETWORKAPI_USE_NEWRELIC', '0') == 1

# Aplicação rodando em modo Debug
DEBUG = os.getenv('NETWORKAPI_DEBUG', '0') == '1'
CI = os.getenv('CI', '0') == '1'

NETWORKAPI_LOG_FILE=os.getenv('NETWORKAPI_LOG_FILE','/tmp/networkapi.log')

# Configuração do arquivo de log do projeto.
LOG_FILE = NETWORKAPI_LOG_FILE

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

# if DEBUG:
#     LOG_LEVEL = logging.DEBUG
# else:
#     LOG_LEVEL = logging.INFO


LOG_DAYS = 10
LOG_SHOW_SQL = False
LOG_DB_LEVEL = logging.DEBUG if LOG_SHOW_SQL else logging.INFO
LOG_USE_STDOUT = False
LOG_SHOW_TRACEBACK = True

# Inicialização do log
# O primeiro parâmetro informa o nome do arquivo de log a ser gerado.
# O segundo parâmetro é o número de dias que os arquivos ficarão mantidos.
# O terceiro parâmetro é o nível de detalhamento do Log.
#Log.init_log(LOG_FILE, LOG_DAYS, LOG_LEVEL, use_stdout=LOG_USE_STDOUT)

if NETWORKAPI_USE_NEWRELIC:
    import newrelic.agent
    config_file_path = os.environ.get('NETWORKAPI_NEW_RELIC_CONFIG')
    if config_file_path is not None:
        newrelic.agent.initialize(config_file_path, os.environ.get('NETWORKAPI_NEW_RELIC_ENV', 'local'))

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

NETWORKAPI_DATABASE_NAME = os.getenv('NETWORKAPI_DATABASE_NAME', 'networkapi')
NETWORKAPI_DATABASE_USER = os.getenv('NETWORKAPI_DATABASE_USER', 'root')
NETWORKAPI_DATABASE_PASSWORD = os.getenv('NETWORKAPI_DATABASE_PASSWORD', '')
NETWORKAPI_DATABASE_HOST = os.getenv('NETWORKAPI_DATABASE_HOST', 'localhost')
NETWORKAPI_DATABASE_PORT = os.getenv('NETWORKAPI_DATABASE_PORT', '3306')
NETWORKAPI_DATABASE_OPTIONS = os.getenv('NETWORKAPI_DATABASE_OPTIONS', '{"init_command": "SET storage_engine=INNODB"}')

# Configurações de banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': NETWORKAPI_DATABASE_HOST,
        'NAME': NETWORKAPI_DATABASE_NAME,
        'USER': NETWORKAPI_DATABASE_USER,
        'PASSWORD': NETWORKAPI_DATABASE_PASSWORD,
        'PORT': NETWORKAPI_DATABASE_PORT,
        'OPTIONS': eval(NETWORKAPI_DATABASE_OPTIONS),
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# CONFIGURAÇÃO DO MEMCACHED
CACHE_BACKEND = 'memcached://localhost:11211/'

NETWORKAPI_MEMCACHE_HOSTS = os.getenv("NETWORKAPI_MEMCACHE_HOSTS",'127.0.0.1:11211')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': NETWORKAPI_MEMCACHE_HOSTS.split(',')
    }
}


# Diretório dos arquivos dos scripts
#SCRIPTS_DIR = os.path.abspath(os.path.join(__file__, '../../scripts'))
SCRIPTS_DIR = os.getenv("NETWORKAPI_SCRIPTS_DIR", os.path.abspath(os.path.join(__file__, '../../scripts')))

# Armazena a raiz do projeto.
SITE_ROOT = os.path.abspath(__file__ + '/../../')

TEMPLATE_DEBUG = DEBUG

API_VERSION = '15.96'

# On create group will associate the 'authenticate' permission
# automatically if 'True'
ASSOCIATE_PERMISSION_AUTOMATICALLY = True
ID_AUTHENTICATE_PERMISSION = 5

NETWORKAPI_SUPPORT_TIME =os.getenv('NETWORKAPI_SUPPORT_TIME',"Suporte Telecom")
NETWORKAPI_SUPPORT_EMAIL=os.getenv('NETWORKAPI_SUPPORT_EMAIL', 'suptel@corp.globo.com')
ADMINS = (
    (NETWORKAPI_SUPPORT_TIME, NETWORKAPI_SUPPORT_EMAIL),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s - U:%(request_user)-6s, P:%(request_path)-8s, T:%(request_id)-6s, MSG:%(message)s',
            'datefmt': '%d/%b/%Y:%H:%M:%S %z',
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
    },
    'filters': {
        'user_filter': {
            '()': 'networkapi.extra_logging.filters.ExtraLoggingFilter',
        }
    },
    'handlers': {
        'log_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose',
            'mode': 'a',
            'filters': ['user_filter'],
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['user_filter'],
        },
    },
    'loggers': {
        'default': {
            'level': LOG_LEVEL,
            'propagate': False,
            'handlers': ['log_file'],
        },
        'django': {
            'level': LOG_LEVEL,
            'propagate': False,
            'handlers': ['log_file'],
        },
        'django.request': {
            'level': LOG_LEVEL,
            'propagate': False,
            'handlers': ['log_file'],
        },
        'django.db.backends': {
            'level': LOG_DB_LEVEL,
            'propagate': False,
            'handlers': ['log_file'],
        },
    },
    'root': {
        'level': LOG_LEVEL,
        'propagate': False,
        'handlers': ['log_file', 'console'],
    },
}


MANAGERS = ADMINS

DEFAULT_CHARSET = 'utf-8'  # Set the encoding to database data


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

NETWORKAPI_TIMEZONE = os.getenv('NETWORKAPI_TIMEZONE','America/Sao_Paulo')
TIME_ZONE = NETWORKAPI_TIMEZONE

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ry@zgop%w80_nu83#!tbz)m&7*i@1)d-+ki@5^d#%6-&^216sg'

VLAN_CACHE_TIME = None
EQUIPMENT_CACHE_TIME = None

# List of callables that know how to import templates from various sources.
if LOG_SHOW_SQL:
    MIDDLEWARE_CLASSES = (
        'networkapi.extra_logging.middleware.ExtraLoggingMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'networkapi.middlewares.SQLLogMiddleware',
        'networkapi.processExceptionMiddleware.LoggingMiddleware',
        'networkapi.middlewares.TrackingRequestOnThreadLocalMiddleware',
    )
else:
    MIDDLEWARE_CLASSES = (
        'networkapi.extra_logging.middleware.ExtraLoggingMiddleware',
        'django.middleware.common.CommonMiddleware',
        'networkapi.processExceptionMiddleware.LoggingMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'networkapi.middlewares.TrackingRequestOnThreadLocalMiddleware',
    )

ROOT_URLCONF = 'networkapi.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.4/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.getenv('NETWORKAPI_STATIC_FILE', SITE_ROOT), 'sitestatic')

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'networkapi', 'templates')
)

INSTALLED_APPS = (
    #'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'networkapi.ambiente',
    'networkapi.equipamento',
    'networkapi.eventlog',
    'networkapi.grupo',
    'networkapi.healthcheckexpect',
    'networkapi.interface',
    'networkapi.ip',
    'networkapi.requisicaovips',
    'networkapi.roteiro',
    'networkapi.tipoacesso',
    'networkapi.usuario',
    'networkapi.vlan',
    'networkapi.grupovirtual',
    'networkapi.models',
    'networkapi.filter',
    'networkapi.filterequiptype',
    'networkapi.blockrules',
    'networkapi.config',
    'networkapi.rack',
    'rest_framework',
    'networkapi.snippets',
    'networkapi.api_pools',
    'networkapi.system',
    'django_extensions',
    'networkapi.api_rack',
)


"""Rest Configuration
"""
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'networkapi.api_rest.authentication.BasicAuthentication',
    ),
}


#DJANGO_SIMPLE_AUDIT_REST_FRAMEWORK_AUTHENTICATOR=BasicAuthentication

NETWORKAPI_VERSION = "1.0"

# Intervals to calculate the vlan_num in POST request /vlan/.
MIN_VLAN_NUMBER_01 = 2
MAX_VLAN_NUMBER_01 = 1001
MIN_VLAN_NUMBER_02 = 1006
MAX_VLAN_NUMBER_02 = 4094

# Intervals to calculate the oct4 of the IP in POST request /ip/.
MIN_OCT4 = 5
MAX_OCT4 = 250

##########
# Scripts

# VLAN
VLAN_REMOVE = 'navlan -i %d --remove'
VLAN_CREATE = 'navlan -I %d -L2 --cria'

# REDE
NETWORKIPV4_CREATE = 'navlan -I %d --IPv4 --cria'
NETWORKIPV6_CREATE = 'navlan -I %d --IPv6 --cria'
NETWORKIPV4_REMOVE = 'navlan -I %d --IPv4 --remove'
NETWORKIPV6_REMOVE = 'navlan -I %d --IPv6 --remove'

VIP_CREATE = 'gerador_vips -i %d --cria'
VIP_REMOVE = 'gerador_vips -i %d --remove'

"""
 Manager Scripts Pool
"""
POOL_CREATE = 'gerador_vips --pool %s --cria'
POOL_REMOVE = 'gerador_vips --pool %s --remove'
POOL_HEALTHCHECK = 'gerador_vips --pool %s --healthcheck'
POOL_REAL_CREATE = 'gerador_vips --pool %s --id_ip %s --port_ip %s --add'
POOL_REAL_REMOVE = 'gerador_vips --pool %s --id_ip %s --port_ip %s --del'
POOL_REAL_ENABLE = 'gerador_vips -p %s --id_ip %s --port_ip %s --ena'
POOL_REAL_DISABLE = 'gerador_vips -p %s --id_ip %s --port_ip %s --dis'
POOL_REAL_CHECK = 'gerador_vips -p %s --id_ip %s --port_ip %s --chk'
POOL_REAL_CHECK_BY_POOL = 'gerador_vips --pool %s --check_status'
POOL_REAL_CHECK_BY_VIP = 'gerador_vips --vip %s --check_status'
POOL_SERVICEDOWNACTION = 'gerador_vips --pool %s --servicedownaction'
POOL_MEMBER_PRIORITIES = 'gerador_vips --pool %s --priority'

# Script to Managemant Status Pool Members
POOL_MANAGEMENT_MEMBERS_STATUS = "gerador_vips --pool %s --apply_status"

# Script to Managemant Status Pool Members
POOL_MANAGEMENT_LB_METHOD = "gerador_vips --pool %s --lb_method"
POOL_MANAGEMENT_LIMITS = "gerador_vips --pool %s --maxconn"


# VIP REAL
VIP_REAL_v4_CREATE = 'gerador_vips -i %s --real %s --ip %s --add'
VIP_REAL_v6_CREATE = 'gerador_vips -i %s --real %s --ipv6 %s --add'
VIP_REAL_v4_REMOVE = 'gerador_vips -i %s --real %s --ip %s --del'
VIP_REAL_v6_REMOVE = 'gerador_vips -i %s --real %s --ipv6 %s --del'
VIP_REAL_v4_ENABLE = 'gerador_vips -i %s --real %s --ip %s --ena'
VIP_REAL_v6_ENABLE = 'gerador_vips -i %s --real %s --ipv6 %s --ena'
VIP_REAL_v4_DISABLE = 'gerador_vips -i %s --real %s --ip %s --dis'
VIP_REAL_v6_DISABLE = 'gerador_vips -i %s --real %s --ipv6 %s --dis'
VIP_REAL_v4_CHECK = 'gerador_vips -i %s --real %s --ip %s --chk'
VIP_REAL_v6_CHECK = 'gerador_vips -i %s --real %s --ipsv6 %s --chk'

# VIP REAL - new calls
VIP_REALS_v4_CREATE = 'gerador_vips -i %s --id_ip %s --port_ip %s --port_vip %s --add'
VIP_REALS_v6_CREATE = 'gerador_vips -i %s --id_ipv6 %s --port_ip %s --port_vip %s --add'
VIP_REALS_v4_REMOVE = 'gerador_vips -i %s --id_ip %s --port_ip %s --port_vip %s --del'
VIP_REALS_v6_REMOVE = 'gerador_vips -i %s --id_ipv6 %s --port_ip %s --port_vip %s --del'
VIP_REALS_v4_ENABLE = 'gerador_vips -i %s --id_ip %s --port_ip %s --port_vip %s --ena'
VIP_REALS_v6_ENABLE = 'gerador_vips -i %s --id_ipv6 %s --port_ip %s --port_vip %s --ena'
VIP_REALS_v4_DISABLE = 'gerador_vips -i %s --id_ip %s --port_ip %s --port_vip %s --dis'
VIP_REALS_v6_DISABLE = 'gerador_vips -i %s --id_ipv6 %s --port_ip %s --port_vip %s --dis'
VIP_REALS_v4_CHECK = 'gerador_vips -i %s --id_ip %s --port_ip %s --port_vip %s --chk'
VIP_REALS_v6_CHECK = 'gerador_vips -i %s --id_ipv6 %s --port_ip %s --port_vip %s --chk'


##################################
#       QUEUE SETTINGS
##################################

BROKER_CONNECT_TIMEOUT=os.getenv('NETWORKAPI_BROKER_CONNECT_TIMEOUT', '2')
BROKER_DESTINATION=os.getenv('NETWORKAPI_BROKER_DESTINATION', "/topic/networkapi_queue")
BROKER_URI=os.getenv('NETWORKAPI_BROKER_URI',u"failover:(tcp://localhost:61613,tcp://server2:61613,tcp://server3:61613)?randomize=falsa,startupMaxReconnectAttempts=2,maxReconnectAttempts=1e")


###################################
#    PATH ACLS
###################################

PATH_ACL = os.path.join(PROJECT_ROOT_PATH, 'ACLS/')

###################################
# PATH RACKS
###################################
#### HARDCODED - MUDA SEMPRE QE ATUALIZARMOS O SO DO TOR
KICKSTART_SO_LF="n6000-uk9-kickstart.7.1.0.N1.1b.bin"
IMAGE_SO_LF="n6000-uk9.7.1.0.N1.1b.bin"
#### <<<<<

PATH_TO_GUIDE = os.getenv('NETWORKAPI_PATH_TO_GUIDE','/vagrant/networkapi/rack/roteiros/')
PATH_TO_ADD_CONFIG = os.getenv('NETWORKAPI_PATH_TO_ADD_GUIDE','/vagrant/networkapi/rack/configuracao/')
PATH_TO_CONFIG = os.getenv('NETWORKAPI_PATH_TO_CONFIG','/vagrant/networkapi/rack/roteiros/')
REL_PATH_TO_CONFIG = os.getenv('NETWORKAPI_REL_PATH_TO_CONFIG','networkapi/rack/roteiros/')
REL_PATH_TO_ADD_CONFIG = os.getenv('NETWORKAPI_REL_PATH_TO_ADD_CONFIG','networkapi/rack/configuracao/')
PATH_TO_MV = os.getenv('NETWORKAPI_PATH_TO_MV','/vagrant/networkapi/rack/roteiros/')

LEAF = "LF-CM"
OOB = "OOB-CM"
SPN = "SPN-CM"
FORMATO = ".cfg"

DIVISAODC_MGMT="OOB-CM"
AMBLOG_MGMT="GERENCIA"
GRPL3_MGMT="CORE/DENSIDADE"

NETWORKAPI_USE_FOREMAN=os.getenv('NETWORKAPI_USE_FOREMAN', '0') == '1'
NETWORKAPI_FOREMAN_URL=os.getenv('NETWORKAPI_FOREMAN_URL','http://foreman_server')

NETWORKAPI_FOREMAN_USERNAME=os.getenv('NETWORKAPI_FOREMAN_USERNAME','admin')
NETWORKAPI_FOREMAN_PASSWORD=os.getenv('NETWORKAPI_FOREMAN_PASSWORD', 'password')

### FOREMAN
USE_FOREMAN=NETWORKAPI_USE_FOREMAN
FOREMAN_URL=NETWORKAPI_FOREMAN_URL
FOREMAN_USERNAME=NETWORKAPI_FOREMAN_USERNAME
FOREMAN_PASSWORD=NETWORKAPI_FOREMAN_PASSWORD
FOREMAN_HOSTS_ENVIRONMENT_ID=1


###################
# TEMPLATE CONFIG #
###################
NETWORKAPI_TFTP_SERVER_ADDR=os.getenv('NETWORKAPI_TFTP_SERVER_ADDR','')

TFTP_SERVER_ADDR = NETWORKAPI_TFTP_SERVER_ADDR

NETWORKAPI_TFTPBOOT_FILES_PATH=os.getenv('NETWORKAPI_TFTPBOOT_FILES_PATH','/mnt/tftpboot/')
TFTPBOOT_FILES_PATH = NETWORKAPI_TFTPBOOT_FILES_PATH


NETWORKAPI_CONFIG_TEMPLATE_PATH=os.getenv('NETWORKAPI_CONFIG_TEMPLATE_PATH','/mnt/config_templates/')
CONFIG_TEMPLATE_PATH = NETWORKAPI_CONFIG_TEMPLATE_PATH

CONFIG_FILES_REL_PATH = "networkapi/generated_config/"
CONFIG_FILES_PATH = TFTPBOOT_FILES_PATH+CONFIG_FILES_REL_PATH
APPLYED_CONFIG_REL_PATH = "networkapi/applyed_config/"

INTERFACE_CONFIG_REL_PATH = "interface/"
#/mnt/config_templates/interface/
INTERFACE_CONFIG_TEMPLATE_PATH = CONFIG_TEMPLATE_PATH+INTERFACE_CONFIG_REL_PATH
#/mnt/tftpboot/networkapi/generated_config/interface/
INTERFACE_CONFIG_FILES_PATH = TFTPBOOT_FILES_PATH+CONFIG_FILES_REL_PATH+INTERFACE_CONFIG_REL_PATH
#networkapi/generated_config/interface/
INTERFACE_CONFIG_TOAPPLY_REL_PATH = CONFIG_FILES_REL_PATH+INTERFACE_CONFIG_REL_PATH

USER_SCRIPTS_REL_PATH = "user_scripts/"
#/mnt/tftpboot/networkapi/generated_config/user_scripts/
USER_SCRIPTS_FILES_PATH = TFTPBOOT_FILES_PATH+CONFIG_FILES_REL_PATH+USER_SCRIPTS_REL_PATH
#networkapi/generated_config/interface/
USER_SCRIPTS_TOAPPLY_REL_PATH = CONFIG_FILES_REL_PATH+USER_SCRIPTS_REL_PATH

NETWORK_CONFIG_REL_PATH = "network/"
#/mnt/config_templates/interface/
NETWORK_CONFIG_TEMPLATE_PATH = CONFIG_TEMPLATE_PATH+NETWORK_CONFIG_REL_PATH
#/mnt/tftpboot/networkapi/generated_config/interface/
NETWORK_CONFIG_FILES_PATH = TFTPBOOT_FILES_PATH+CONFIG_FILES_REL_PATH+NETWORK_CONFIG_REL_PATH
#networkapi/generated_config/interface/
NETWORK_CONFIG_TOAPPLY_REL_PATH = CONFIG_FILES_REL_PATH+NETWORK_CONFIG_REL_PATH
###################


## TESTS CONFIGS ##
# If is running on CI: if CI=1 or running inside jenkins
INTEGRATION = os.getenv('CI', '0') == '1'
INTEGRATION_TEST_URL = os.getenv('INTEGRATION_TEST_URL', 'http://localhost')

TEST_DISCOVER_ROOT = os.path.abspath(os.path.join(__file__, '..'))

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=2', '--no-byte-compile', '-d', '-s']
if CI:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
            },
        },
        'handlers': {
            'console':{
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django': {
                'handlers':['console'],
                'propagate': False,
                'level':'INFO',
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.db.backends': {
                'level': 'INFO',
                'propagate': False,
                'handlers': ['console'],
            },
        },
        'root': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['console'],
        },
    }
    INSTALLED_APPS += ('django_nose',)
    NOSE_ARGS += ['--with-coverage', '--cover-package=networkapi',
                  '--exclude=.*migrations*', '--exclude-dir=./integration/',
                  '--with-xunit', '--xunit-file=test-report.xml', '--cover-xml', '--cover-xml-file=coverage.xml']

# elif INTEGRATION:
#     TEST_DISCOVER_ROOT = None
#     NOSE_ARGS += ['--with-coverage', '--cover-package=networkapi', '--where-dir=./integration/',
#                   '--with-xunit', '--xunit-file=test-report.xml', '--cover-xml', '--cover-xml-file=coverage.xml']

