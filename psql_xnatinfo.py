__author__ = 'damons'
__email__ = 'stephen.m.damon@vanderbilt.edu'
__purpose__ = "Run Xnatinfo on the database."
__version__ = '1.0.0'
__modifications__ = '13 August 2015 - Original write' \
                    '26 August 2015 - Remove host since only running on localhost'
__todo__ = ['Add in scans', 'Add in sessions/subjects/assessors', 'Add in scan type']
import psycopg2
from psycopg2 import OperationalError
import sys
from copy import deepcopy

# Select all the assessors
SELECT_CALL = "SELECT proctype, procstatus FROM proc_genprocdata WHERE id IN (SELECT id FROM xnat_experimentData WHERE project='%s' AND label LIKE '%s-x-%%')"


def parse_args():
    """Set up the ArgumentParser"""

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-p', '--project', dest='project',
                   help='Project ID on XNAT', required=True)
    p.add_argument('-u', '--user', dest='user', help='DB owner username',
                   required=True)
    p.add_argument('-d', '--dbname', dest='dbname',
                   help='Database name', required=True)
    p.add_argument('-c', '--cred', dest='password',
                   help='Database username password', required=True)
    return p.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    # Try to connect and exit if we catch the most common OperationalError
    # will add more as they are encountered.
    try:
        conn = psycopg2.connect(dbname=ARGS.dbname,
                                password=ARGS.password, user=ARGS.user)
    except OperationalError as operr:
        print "FATAL: Caught an OperationalError. Please check your dbname, " \
              "host ip address, username, and password"
        sys.exit(1)

    cur = conn.cursor()
    cur.execute(SELECT_CALL % (ARGS.project, ARGS.project))
    result = cur.fetchall()
    # count, complete, ready_to_complete, uploading, ready_to_upload, job_failed, job_running, NEED_TO_RUN, need_inputs, no_data, unknown
    COUNT = [0,0,0,0,0,0,0,0,0,0,0]
    procs = {}
    known_list = ['COMPLETE', 'READY_TO_COMPLETE', 'UPLOADING', 'READY_TO_UPLOAD', 'JOB_FAILED', 'JOB_RUNNING', 'NEED_TO_RUN', 'NEED_INPUTS', 'NO_DATA']
    i=0
    # This is gross and needs some TLC
    for r in result:
        if r[0] not in procs.keys():
            procs[r[0]] = deepcopy(COUNT)

        if r[1] == 'COMPLETE':
            procs[r[0]][1] = procs[r[0]][1] +1
            procs[r[0]][0] +=1
        elif r[1] == 'READY_TO_COMPLETE':
            procs[r[0]][2] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'UPLOADING':
            procs[r[0]][3] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'READY_TO_UPLOAD':
            procs[r[0]][4] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'JOB_FAILED':
            procs[r[0]][5] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'JOB_RUNNING':
            procs[r[0]][6] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'NEED_TO_RUN':
            procs[r[0]][7] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'NEED_INPUTS':
            procs[r[0]][8] +=1
            procs[r[0]][0] +=1
        elif r[1] == 'NO_DATA':
            procs[r[0]][9] +=1
            procs[r[0]][0] +=1
        else:
            procs[r[0]][10] +=1
            procs[r[0]][0] +=1
        i+=1


    aslen = 25
    for key in procs.keys():
        if key is not None:
            if len(key) > aslen:
                aslen=len(key)

    print '  %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s ' % (-1*aslen, 'Process type', -5, 'Count',-8,'COMPLETE',-17, 'READY_TO_COMPLETE',-9,    'UPLOADING',-15, 'READY_TO_UPLOAD',-10, 'JOB_FAILED',-11,'JOB_RUNNING',-11, 'NEED_TO_RUN',-11, 'NEED_INPUTS',-7,'NO_DATA',-7,'UNKNOWN')
    for key in sorted(procs) :
        print '  %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s | %*s ' % (-1*aslen, key, -5, procs[key][0], -8, procs[key][1], -17, procs[key][2],-9, procs[key][3],-15, procs[key][4],-10, procs[key][5],-11, procs[key][6],-11, procs[key][7],-11, procs[key][8],-7, procs[key][9],-7, procs[key][10])


