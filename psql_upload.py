__author__ = 'damons'


import psycopg2
import datetime
import os
import paramiko
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

def get_xdat_change_info_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_abstractresource_xnat_abstractresource_id_seq')""");
    result = cursor.fetchone()
    return result[0].__int__()

def get_meta_data_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_resource_meta_data_meta_data_id_seq')""");
    result = cursor.fetchone()
    return result[0].__int__()

def get_meta_data_id2(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_abstractresource_meta_data_meta_data_id_seq')""");
    result = cursor.fetchone()
    return result[0].__int__()

def get_xnat_abstractresource_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_abstractresource_xnat_abstractresource_id_seq')""");
    result = cursor.fetchone()
    return result[0].__int__()

def get_resourcecatalog_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_resourcecatalog_meta_data_meta_data_id_seq')""");
    result = cursor.fetchone()
    return result[0].__int__()
def get_timestamp():
    """
    :return: timestamp
    """
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def insert_xnat_resource_meta_data(conn,cursor,xft_version,meta_data_id):
    """

    :param cursor:
    :return:
    """
    date=get_timestamp()
    print date
    cursor.execute("""INSERT INTO xnat_resource_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES (%s,'active',1,'%s','%s','%s',0,1,%s,1)""" %(xft_version,date,date,date,meta_data_id))
    conn.commit()
def insert_xnat_abstractResource_meta_data(conn,cursor,xft_version,meta_data_id):
    """

    :param cursor:
    :return:
    """
    date=get_timestamp()
    print date
    cursor.execute("""INSERT INTO xnat_abstractResource_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES (%s,'active',1,'%s','%s','%s',0,1,%s,1)""" %(xft_version,date,date,date,meta_data_id))
    conn.commit()

def insert_xnat_abstractResource(conn,cursor,abstractresource_info,xnat_abstractresource_id,resource_name):
    """

    :param cursor:
    :return:
    """
    date=get_timestamp()
    print date
    cursor.execute("""INSERT INTO xnat_abstractResource (abstractresource_info,xnat_abstractresource_id,label,extension) VALUES (%s,%s,'%s',234)""" % (abstractresource_info,xnat_abstractresource_id,resource_name))
    conn.commit()

def insert_xnat_resource(conn,cursor,xnat_abstractresource_id,resource_info,uri):
    """

    :param cursor:
    :param xnat_abstractresource_id:
    :param resource_info:
    :param uri:
    :return:
    """
    cursor.execute("""INSERT INTO xnat_resource (xnat_abstractresource_id,resource_info,uri) VALUES (%s,%s,'%s')""" %(xnat_abstractresource_id,resource_info,uri))
    conn.commit()

def insert_xnat_resourceCatalog_meta_data(conn,cursor,xft_version,meta_data_id):
    """

    :param cursor:
    :return:
    """
    date=get_timestamp()
    print date
    cursor.execute("""INSERT INTO xnat_resourceCatalog_meta_data(xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES ('%s','active',1,'%s','%s','%s',0,1,%s,1)""" %(xft_version,date,date,date,meta_data_id))
    conn.commit()

def insert_xnat_resourceCatalog(conn,cursor,xnat_abstractresource_id, resourcecatalog_info):
    """

    :param cursor:
    :param xnat_abstractresource_id:
    :param resourcecatalog_info:
    :return:
    """
    cursor.execute("""INSERT INTO xnat_resourceCatalog (xnat_abstractresource_id,resourcecatalog_info) VALUES (%s,%s)"""%(xnat_abstractresource_id,resourcecatalog_info))
    conn.commit()

def insert_img_assessor_out_resource(conn,cursor,assessor_id,xnat_abstractresource_id):
    """

    :param cursor:
    :param assessor_id:
    :param xnat_abstractresource_id:
    :return:
    """
    cursor.execute("""INSERT INTO img_assessor_out_resource (xnat_imageAssessorData_id,xnat_abstractResource_xnat_abstractresource_id) VALUES ('%s',%s)""" %(assessor_id,xnat_abstractresource_id))
    conn.commit()

def load_queue(upload_dir):
    dirs = os.listdir(upload_dir)
    known_bad = ['TRASH', 'DISKQ','FlagFiles','PBS','TRASH', 'OUTLOG']
    for known in known_bad:
        if known in dirs:
            dirs.remove(known)
    return dirs

def get_assessor_id_from_assessor_label(cursor,assessor):
    """
:
    :param assessor:
    :return:
    """
    cursor.execute("""SELECT id from xnat_experimentdata where label=('%s')""" % assessor)
    result = cursor.fetchone()
    try:
        return result[0]
    except TypeError as te:
        return None


def get_archive_path(cursor,project_id):
    """

    :param cursor:
    :param project_id:
    :return:
    """
    cursor.execute("""SELECT archivepath from arc_pathinfo where archivepath LIKE '%%/%s/'""" % project_id)
    return cursor.fetchone()

def mkdir_p(sftp, remote_directory):
    print remote_directory
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == '/':
        # absolute path so change directory to root
        sftp.chdir('/')
        return
    if remote_directory == '':
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory) # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        print basename
        mkdir_p(sftp, dirname) # make parent directories
        sftp.mkdir(basename) # sub-directory missing, so created it
        sftp.chdir(basename)
        return True




if __name__ == '__main__':
    ARGS = parse_args()
    ssh = paramiko.Transport('129.59.91.137',22)
    ssh.connect(username='', password='')
    sftp = paramiko.SFTPClient.from_transport(ssh)

    # Try to connect and exit if we catch the most common OperationalError
    # will add more as they are encountered.
    conn = psycopg2.connect(dbname=ARGS.dbname,
                                password=ARGS.password, user=ARGS.user,
                                host='')

    cursor = conn.cursor()
    upload_dir =''
    queue = load_queue(upload_dir)
    for assessor in queue:
        print "Begin assessor %s" % assessor
        fullpath = os.path.join(upload_dir,assessor)
        if os.path.exists(os.path.join(fullpath,'READY_TO_UPLOAD.txt')):
            print "\tREADY flag exists. Begin upload"
            assessor_id = get_assessor_id_from_assessor_label(cursor,assessor)
            if assessor_id is None:
                print "\tAssessor %s does not exist. Skipping..." % assessor
                continue
            archive_path = get_archive_path(cursor,assessor.split('-x-')[0])
            if not archive_path:
                print "Could not fetch archive path for project %s" % assessor.split('-x-')[0]
                continue
            resources = os.listdir(fullpath)
            for resource in resources:
                if os.path.isdir(os.path.join(fullpath,resource)):
                    os.chdir(os.path.join(fullpath,resource))
                    for f in os.walk('.'):
                        #mkdir_p(sftp,f[0].replace(archive_))
                        tail_of_dir = f[0].replace(archive_path[0],'')
                        uri = os.path.join(archive_path[0],'arc001',assessor.split('-x-')[1],'ASSESSORS',assessor,resource,tail_of_dir)
                        print uri
                        mkdir_p(sftp,uri)
                        for fl in f[2]:
                            sftp.put(os.path.join(f[0],fl),os.path.join(uri,fl))



                xft_version = get_xdat_change_info_id(cursor)
                meta_data_id =get_meta_data_id(cursor)
                abstract_meta_data_id = get_meta_data_id2(cursor)
                xnat_abstractresource_id = get_xnat_abstractresource_id(cursor)
                resroucecatalog_id = get_resourcecatalog_id(cursor)

                # xnat_resource_meta_data
                insert_xnat_resource_meta_data(conn,cursor,xft_version,meta_data_id)
                insert_xnat_abstractResource_meta_data(conn,cursor,xft_version,meta_data_id)
                insert_xnat_abstractResource(conn,cursor,abstract_meta_data_id,xnat_abstractresource_id,resource)
                uri = '%sarc001/%s/ASSESSORS/%s/%s/%s_catalog.xml' % (archive_path,
                                                                      assessor.split('-x-')[2],
                                                                      assessor,
                                                                      resource,
                                                                      resource)
                insert_xnat_resourceCatalog_meta_data(conn,cursor,xft_version,meta_data_id)
                insert_xnat_resource(conn,cursor,xnat_abstractresource_id,resroucecatalog_id,uri)
                insert_xnat_resourceCatalog(conn,cursor,xnat_abstractresource_id,resroucecatalog_id)
                insert_img_assessor_out_resource(conn,cursor,assessor_id,xnat_abstractresource_id)
        else:
            print "\tREADY flag does NOT exist. skipping..."
