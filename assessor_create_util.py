__author__ = 'damons'
import psycopg2
import sys
import re
import datetime

def get_connection(dbname='xnat', user='xnat', password=''):
    """

    :param dbname:
    :param user:
    :param password:
    :return:
    """
    try:
     conn = psycopg2.connect(dbname=dbname,
                             password=password, user=user,
                             host='masijenkins.vuse.vanderbilt.edu')
    except psycopg2.OperationalError:
     print "FATAL: Caught an OperationalError. Please check your dbname, " \
           "host ip address, username, and password"
     sys.exit(1)
    return conn

def get_cursor(connection):
    """

    :param connection:
    :return:
    """

    return connection.cursor()

def get_xdat_change_info_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xdat_change_info_xdat_change_info_id_seq') AS xdat_change_info_id""")
    result = cursor.fetchall()
    return result[0]

def get_experimentdata_meta_data_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_experimentdata_meta_data_meta_data_id_seq') AS meta_data_id""")
    result = cursor.fetchall()
    return result[0]

def ie_xnat_deriveddata(cursor, experiment_id):
    """

    :param cursor:
    :param experiment_id:
    :return:
    """
    cmd = """SELECT ie_xnat_derivedData((%s),0,FALSE,TRUE,false)"""
    cursor.execute(cmd, experiment_id)
    result = cursor.fetchall()
    return result
def get_deriveddata_meta_data_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_deriveddata_meta_data_meta_data_id_seq') AS meta_data_id""")
    result = cursor.fetchall()
    return result[0]

def ie_xnat_imageassessordata(cursor, experiment_id):
    """

    :param cursor:
    :param experiment_id:
    :return:
    """
    cmd = """SELECT ie_xnat_imageAssessorData((%s),0,FALSE,TRUE,false)"""
    cursor.execute(cmd, experiment_id)
    result = cursor.fetchall()
    return result

def get_imageassesordata_meta_data_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.xnat_imageassessordata_meta_data_meta_data_id_seq') AS meta_data_id""")
    result = cursor.fetchall()
    return result[0]

def i_proc_genprocdata(cursor, experiment_id):
    """

    :param cursor:
    :param experiment_id:
    :return:
    """
    cmd = """SELECT i_proc_genProcData('DEV_VUIISXNAT_E00003',0,FALSE,TRUE,false)"""
    cursor.execute(cmd, experiment_id)
    result = cursor.fetchall()
    return result

def get_procgenprocdata_meta_data_id(cursor):
    """

    :param cursor:
    :return:
    """
    cursor.execute("""SELECT nextval('public.proc_genprocdata_meta_data_meta_data_id_seq') AS meta_data_id""")
    result = cursor.fetchall()
    return result[0]

def insert_xnat_experimentdata_meta_data(conn, cursor, xft_version, meta_data_id):
    """

    :param cursor:
    :param xft_version:
    :param activation_date:
    :param row_last_modified:
    :param insert_date:
    :param meta_data_id:
    :return:
    """

    activation_date = get_timestamp()
    row_last_modified = activation_date
    insert_date = activation_date
    cmd = """INSERT INTO xnat_experimentData_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES ((%s),'active',1,(%s),(%s),(%s),0,1,(%s),1)"""
    cursor.execute(cmd, (xft_version, activation_date, row_last_modified, insert_date, meta_data_id))
    conn.commit()

def insert_xnat_experimentdata(conn, cursor, experimentdata_info, label, project, id):
    """

    :param cursor:
    :return:
    """
    cmd="""INSERT INTO xnat_experimentData (experimentdata_info,label,project,extension,id) VALUES ((%s),(%s),(%s),586,(%s))"""
    cursor.execute(cmd,(str(experimentdata_info[0].__int__()),
                         label,
                         project,
                         id))
    conn.commit()

def insert_xnat_deriveddata_meta_data(conn, cursor, xft_version, meta_data_id):
    """

    :param conn:
    :param cursor:
    :param xft_version:
    :param meta_data_id:
    :return:
    """
    activation_date = get_timestamp()
    row_last_modified = activation_date
    insert_date = activation_date
    cmd="""INSERT INTO xnat_derivedData_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES ((%s),'active',1,(%s),(%s),(%s),0,1,(%s),1)"""
    cursor.execute(cmd, (xft_version, activation_date, row_last_modified, insert_date, meta_data_id))
    conn.commit()

def insert_xnat_deriveddata(conn, cursor, deriveddata_info,experiment_id):
    """

    :param cursor:
    :return:
    """
    cmd="""INSERT INTO xnat_derivedData (deriveddata_info,id) VALUES ((%s),(%s))"""
    cursor.execute(cmd, (deriveddata_info, experiment_id))
    conn.commit()

def insert_xnat_imageassessordata_meta_data(conn,cursor, xft_version, meta_data_id):
    """

    :param cursor:
    :return:
    """
    activation_date = get_timestamp()
    row_last_modified = activation_date
    insert_date = activation_date
    cmd = """INSERT INTO xnat_imageAssessorData_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES ((%s),'active',1,(%s),(%s),(%s),0,1,(%s),1)"""
    cursor.execute(cmd, (xft_version, activation_date, row_last_modified, insert_date, meta_data_id))
    conn.commit()

def insert_xnat_imageassessordata(conn, cursor, meta_data_id, assessor_id, session_id):
    """

    :param cusor:
    :return:
    """
    cmd = """INSERT INTO xnat_imageAssessorData (imageassessordata_info,id,imagesession_id) VALUES ((%s),(%s),(%s))"""
    cursor.execute(cmd, (meta_data_id, assessor_id, session_id))
    conn.commit()

def insert_proc_genrocdata_meta_data(conn,cursor, xft_version, meta_data_id):
    """

    :param cursor:
    :return:
    """
    activation_date = get_timestamp()
    row_last_modified = activation_date
    insert_date = activation_date
    cmd = """INSERT INTO proc_genProcData_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES ((%s),'active',1,(%s),(%s),(%s),0,1,(%s),1)"""
    cursor.execute(cmd, (xft_version, activation_date, row_last_modified, insert_date, meta_data_id))
    conn.commit()

def insert_proc_genrocdata(conn, cursor, meta_data_id, experiment_id):
    """

    :param cursor:
    :return:
    """
    cmd = """INSERT INTO proc_genProcData (genprocdata_info,id) VALUES ((%s),(%s))"""
    cursor.execute(cmd, (meta_data_id, experiment_id))
    conn.commit()

def update_proc_genprocdata_meta_data(cursor):
    """

    :param cursor:
    :return:
    """
    cmd = """UPDATE proc_genProcData_meta_data SET last_modified='2016-04-12 13:50:06.283', modified=1 WHERE meta_data_id=1 """

def insert_xdat_change_info(cursor):
    """

    :param cursor:
    :return:
    """
    cmd = """INSERT INTO xdat_change_info (xdat_change_info_id,change_user,change_date,event_id) VALUES (805,1,'2016-04-12 13:50:06.022',101)"""

def update_ls_proc_genprocdata(cursor):
    """

    :param cursor:
    :return:
    """
    cmd = """SELECT update_ls_proc_genProcData('DEV_VUIISXNAT_E00003',1)"""

def i_wkr_workflowdata(cursor):
    """

    :param cursor:
    :return:
    """

def get_next_experiment_id(cursor):
    """
    These IDs should really be some sort of serial8 or something of the like,
    but this sorts the tuple to get the max value and then adds
    :param cursor:
    :param subject_ids:
    :return: the new ID (in a tuple)
    """
    cmd = """SELECT DISTINCT id FROM (SELECT id FROM xnat_experimentData WHERE id LIKE 'DEV_VUIISXNAT_E%' UNION SELECT DISTINCT id FROM xnat_experimentData_history WHERE id LIKE 'DEV_VUIISXNAT_E%') SRCHA"""
    cursor.execute(cmd)
    experiment_ids = cursor.fetchall()
    # Sort here rather than using postgres to mimic XNAT
    experiment_ids.sort()
    last_id = experiment_ids[len(experiment_ids)-1]

    # I don't know if numbers are OK in the XNAT instance name. Thus, split the
    #  '_' and take the last element
    tail_of_id = last_id[0].split('_')
    last_id_digits = re.findall(r'\d+', tail_of_id[len(tail_of_id)-1])

    # pop the last element of the tail_of_id to reconstruct the XNAT instance name
    tail_of_id.pop(len(tail_of_id)-1)

    # I don't know if the zeropadding is a hard limit. This mimics the current install
    id = "%s_E%05d" % ('_'.join(tail_of_id), int(last_id_digits[0])+1)
    return (id,)


def get_timestamp():
    """
    :return: timestamp
    """
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def get_timestamp_from_datetime_object(obj):
    """

    :param obj:
    :return:
    """
    return obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]