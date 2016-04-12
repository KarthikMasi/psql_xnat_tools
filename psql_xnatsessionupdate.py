__author__ = 'damons'
__email__ = 'stephen.m.damon@vanderbilt.edu'
__purpose__ = "Run Xnatsessionupdate on the database. This gives a " \
              "HUGE improvement rather than using pyxnat's set method" \
              "time Xnatsessionupdate -p VUSTP -a:" \
              "     real	0m40.719s" \
              "     user	0m0.547s" \
              "     sys	    0m0.152s" \
              "time psql_xnatsessionupdate -p VUSTP -a ...:" \
              "     real	0m3.341s" \
              "     user	0m0.410s" \
              "     sys	    0m0.133s"
__version__ = '1.0.0'
__modifications__ = '13 August 2015 - Original write' \
                    '26 August 2015 - Remove host since only running on localhost' \
                    '27 August 2015 - Add in autocommit=True to autoexecute calls on an execute command' \
                    '               - semantics fix' \
                    '               - strip out XnatUtils and get all session labels from the db.'

import psycopg2
from psycopg2 import OperationalError
import sys

# This call is just for debugging to make sure it worked.
# Probably won't ever be used
SELECT_CALL = "SELECT original FROM xnat_experimentData WHERE project='%s' AND label IN (%s);"

# This call is used to update the database
UPDATE_CALL_USER = "UPDATE xnat_experimentData SET original=' ' WHERE project='%s' AND label IN (%s);"

# If the user wants to run all of the sessions, grab them via the database and not XnatUtils
UPDATE_CALL_ALL = "UPDATE xnat_experimentData SET original=' ' WHERE project='%s' AND label IN " \
                  "(SELECT label FROM xnat_experimentData WHERE project='%s' AND label NOT LIKE '%s-x-%%');"
def parse_args():
    """Set up the ArgumentParser"""

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-p', '--project', dest='project',
                   help='Project ID on XNAT', required=True)
    p.add_argument('-s', '--session', dest='session',
                   help='Session(s) on Xnat. Comma separate if multiple',
                   required=False)
    p.add_argument('-a', '--all', dest='all',
                   help='Reset all sessions in the project',
                   action='store_true',
                   default=False)
    p.add_argument('-u', '--user', dest='user', help='DB owner username',
                   required=True)
    p.add_argument('-d', '--dbname', dest='dbname',
                   help='Database name', required=True)
    p.add_argument('-c', '--cred', dest='password',
                   help='Database username password', required=True)
    return p.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    if ARGS.session:
        USER_SESSIONS = ARGS.session.split(',')

    # Try to connect and exit if we catch the most common OperationalError
    # will add more as they are encountered.
    try:
        conn = psycopg2.connect(dbname=ARGS.dbname,
                                password=ARGS.password, user=ARGS.user)
        conn.autocommit = True
    except OperationalError as operr:
        print "FATAL: Caught an OperationalError. Please check your dbname, " \
              "host ip address, username, and password"
        sys.exit(1)

    cur = conn.cursor()

    if ARGS.all:
        # Grab every session from the project and reset
        cur.execute(UPDATE_CALL_ALL % (ARGS.project, ARGS.project, ARGS.project))

    else:
        # We assume the user gave the correct sessions.
        # TODO run the query to make sure these are all correct
        SESSIONS = USER_SESSIONS

        # *************** BEGIN debugging code
        # cur.execute(SELECT_CALL % (ARGS.project, (','.join("'" + item + "'" for item in SESSIONS))))
        # res= cur.fetchall()
        # for r in res:
        #     print r
        # *************** END debugging code
        cur.execute(UPDATE_CALL_USER % (ARGS.project, (','.join("'" + item + "'" for item in SESSIONS))))
