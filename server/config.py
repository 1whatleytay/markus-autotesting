#!/usr/bin/env python3

#### CHANGE CONFIG PARAMETERS BELOW ####

## REDIS CONFIGS ##

# name of redis hash used to store the locations of test script directories
REDIS_CURRENT_TEST_SCRIPT_HASH = 'curr_test_scripts'
# name of redis hash used to store pop interval data for each worker queue 
REDIS_POP_HASH = 'pop_intervals'
# name of redis hash used to store workers data (username and worker directory)
REDIS_WORKERS_HASH = 'workers'
# name of redis integer used to access the next available port
REDIS_PORT_INT = 'ports'
# dictionary containing keyword arguments to pass to rq.use_connection 
# when connecting to a redis database (empty dictionary is default)
REDIS_CONNECTION_KWARGS = {}
# prefix to prepend to all redis keys generated by the autotester
REDIS_PREFIX = 'autotest:'
# prefix to prepend to all postgres databases created
POSTGRES_PREFIX = 'autotest_'

## WORKING DIR CONFIGS ##

# the main working directory
WORKSPACE_DIR = '/home/vagrant/markus-autotesting/server/workspace'
# name of the directory containing test scripts
SCRIPTS_DIR_NAME = 'scripts'
# name of the directory containing test results
RESULTS_DIR_NAME = 'results'
# name of the directory containing specs files
SPECS_DIR_NAME = 'specs'
# name of the directory containing workspaces for the workers
WORKERS_DIR_NAME = 'workers'
# name of the directory containing log files 
LOGS_DIR_NAME = 'logs'
# name of the server user
SERVER_USER = ''
# names of the worker users
WORKER_USERS = 'autotst0 autotst1 autotst2 autotst3 autotst4 autotst5 autotst6 autotst7'
# prefix used to name reaper users 
# (reapers not used to kill worker processes if set to the empty string)
REAPER_USER_PREFIX = ''
# default tester environment name
DEFAULT_ENV_NAME = 'defaultenv'

## RLIMIT SETTINGS FOR TESTER PROCESSES ##

# values are: (soft limit, hard limit)
# see https://docs.python.org/3/library/resource.html for reference on limit options
# NOTE: these limits cannot be higher than the limits set for the tester user in
#       /etc/security/limits.conf (or similar). These limits may be reduced in certain
#       cases (see the docstring for get_test_preexec_fn and get_cleanup_preexec_fn in
#       autotest_server.py)
RLIMIT_SETTINGS = {
    'RLIMIT_NPROC': (300, 300)
}

### QUEUE CONFIGS ###

# functions used to select which type of queue to use. They must accept any number
# of keyword arguments and should only return a boolean (see autotest_enqueuer._get_queue)
def batch_filter(**kwargs):
    return kwargs.get('batch_id') is not None

def single_filter(**kwargs):
    return kwargs.get('user_type') == 'Admin' and not batch_filter(**kwargs)

def student_filter(**kwargs):
    return kwargs.get('user_type') == 'Student' and not batch_filter(**kwargs)

# list of worker queues. Values of each are a string indicating the queue name,
# and a function used to select whether or not to use this type of queue 
# (see autotest_enqueuer._get_queue)
batch_queue = {'name': 'batch', 'filter': batch_filter}
single_queue = {'name': 'single', 'filter': single_filter}
student_queue = {'name': 'student', 'filter': student_filter}
WORKER_QUEUES = [batch_queue, single_queue, student_queue]

### WORKER CONFIGS ###

WORKERS = [(4, [student_queue['name'], single_queue['name'], batch_queue['name']]),
           (2, [single_queue['name'], student_queue['name'], batch_queue['name']]),
           (2, [batch_queue['name'], student_queue['name'], single_queue['name']])]
