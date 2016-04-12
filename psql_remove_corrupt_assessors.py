__author__ = 'damons'
__purpose__ = 'Every now and then a database transaction trashes and leaves a project in a perpetually ' \
              'corrupt state the purpose of this script is to find those and delete them'

from dax import XnatUtils
import psycopg2
import sys
from psycopg2 import OperationalError

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

    XNAT = XnatUtils.get_interface()
    PROJECTS = XNAT.select('/projects').get()

    for PROJECT in PROJECTS:
        sessions = XnatUtils.list_experiments(XNAT, PROJECT)
        for session in sessions:
            if '-x-' in session['session_label']:
                sys.stdout.write('Found corrupt assessors %s for project %s\n' % (session['session_label'],
                                                                                  PROJECT))
                cur.execute("""DELETE FROM xnat_experimentdata where label=(%s)""",(session['session_label'],))
                conn.commit()
    XNAT.disconnect()
    conn.close()