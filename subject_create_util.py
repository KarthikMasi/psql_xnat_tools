__author__ = 'damons'
__purpose__ = 'I scratched and itch to burst generate subjects. NOTE THIS ONLY RUNS AS ADMIN'
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
 except psycopg2.OperationalError as operr:
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

def check_if_subject_label_exists(cursor, project_id, subject_label):
 """
 Method to check and see if a subject LABEL exists.
 :param cursor:
 :param project_id:
 :param subject_label:
 :return:
 """
 cmd = """SELECT xnat_subjectData.id AS xnat_subjectData3, xnat_subjectData.investigator_xnat_investigatordata_id AS xnat_subjectData0, xnat_subjectData.demographics_xnat_abstractdemographicdata_id AS xnat_subjectData1, xnat_subjectData.metadata_xnat_abstractsubjectmetadata_id AS xnat_subjectData2, xnat_subjectData.project AS xnat_subjectData4, xnat_subjectData._group AS xnat_subjectData5, xnat_subjectData.label AS xnat_subjectData6, xnat_subjectData.src AS xnat_subjectData7, xnat_subjectData.initials AS xnat_subjectData8, xnat_subjectData.subjectdata_info AS xnat_subjectData9, table1.title AS xnat_investigatorData67, table1.firstname AS xnat_investigatorData68, table1.lastname AS xnat_investigatorData69, table1.institution AS xnat_investigatorData70, table1.department AS xnat_investigatorData71, table1.email AS xnat_investigatorData72, table1.phone AS xnat_investigatorData73, table1.id AS xnat_investigatorData74, table1.investigatordata_info AS xnat_investigatorData75, table1.xnat_investigatordata_id AS xnat_investigatorData76, table2.xft_version AS xnat_investigatorData_meta_data77, table2.last_modified AS xnat_investigatorData_meta_data78, table2.status AS xnat_investigatorData_meta_data79, table2.activation_date AS xnat_investigatorData_meta_data80, table2.row_last_modified AS xnat_investigatorData_meta_data81, table2.insert_date AS xnat_investigatorData_meta_data82, table2.activation_user_xdat_user_id AS xnat_investigatorData_meta_data83, table2.insert_user_xdat_user_id AS xnat_investigatorData_meta_data84, table2.origin AS xnat_investigatorData_meta_data85, table2.modified AS xnat_investigatorData_meta_data86, table2.shareable AS xnat_investigatorData_meta_data87, table2.meta_data_id AS xnat_investigatorData_meta_data88, table3.extension AS xnat_abstractDemographicData89, table3.abstractdemographicdata_info AS xnat_abstractDemographicData90, table3.xnat_abstractdemographicdata_id AS xnat_abstractDemographicData91, table4.element_name AS xdat_meta_element92, table4.xdat_meta_element_id AS xdat_meta_element93, table5.xft_version AS xnat_abstractDemographicData_meta_data94, table5.last_modified AS xnat_abstractDemographicData_meta_data95, table5.status AS xnat_abstractDemographicData_meta_data96, table5.activation_date AS xnat_abstractDemographicData_meta_data97, table5.row_last_modified AS xnat_abstractDemographicData_meta_data98, table5.insert_date AS xnat_abstractDemographicData_meta_data99, table5.activation_user_xdat_user_id AS xnat_abstractDemographicData_meta_data100, table5.insert_user_xdat_user_id AS xnat_abstractDemographicData_meta_data101, table5.origin AS xnat_abstractDemographicData_meta_data102, table5.modified AS xnat_abstractDemographicData_meta_data103, table5.shareable AS xnat_abstractDemographicData_meta_data104, table5.meta_data_id AS xnat_abstractDemographicData_meta_data105, table6.extension AS xnat_abstractSubjectMetadata106, table6.abstractsubjectmetadata_info AS xnat_abstractSubjectMetadata107, table6.xnat_abstractsubjectmetadata_id AS xnat_abstractSubjectMetadata108, table7.element_name AS xdat_meta_element109, table7.xdat_meta_element_id AS xdat_meta_element110, table8.xft_version AS xnat_abstractSubjectMetadata_meta_data111, table8.last_modified AS xnat_abstractSubjectMetadata_meta_data112, table8.status AS xnat_abstractSubjectMetadata_meta_data113, table8.activation_date AS xnat_abstractSubjectMetadata_meta_data114, table8.row_last_modified AS xnat_abstractSubjectMetadata_meta_data115, table8.insert_date AS xnat_abstractSubjectMetadata_meta_data116, table8.activation_user_xdat_user_id AS xnat_abstractSubjectMetadata_meta_data117, table8.insert_user_xdat_user_id AS xnat_abstractSubjectMetadata_meta_data118, table8.origin AS xnat_abstractSubjectMetadata_meta_data119, table8.modified AS xnat_abstractSubjectMetadata_meta_data120, table8.shareable AS xnat_abstractSubjectMetadata_meta_data121, table8.meta_data_id AS xnat_abstractSubjectMetadata_meta_data122, table9.xft_version AS xnat_subjectData_meta_data323, table9.last_modified AS xnat_subjectData_meta_data324, table9.status AS xnat_subjectData_meta_data325, table9.activation_date AS xnat_subjectData_meta_data326, table9.row_last_modified AS xnat_subjectData_meta_data327, table9.insert_date AS xnat_subjectData_meta_data328, table9.activation_user_xdat_user_id AS xnat_subjectData_meta_data329, table9.insert_user_xdat_user_id AS xnat_subjectData_meta_data330, table9.origin AS xnat_subjectData_meta_data331, table9.modified AS xnat_subjectData_meta_data332, table9.shareable AS xnat_subjectData_meta_data333, table9.meta_data_id AS xnat_subjectData_meta_data334 FROM (SELECT SEARCH.* FROM (SELECT DISTINCT ON (xnat_subjectData3) * FROM (SELECT xnat_subjectData.id AS xnat_subjectData3, xnat_subjectData.project AS xnat_subjectData4, xnat_subjectData.label AS xnat_subjectData6, table1.project AS xnat_projectParticipant11 FROM xnat_subjectData xnat_subjectData   LEFT JOIN xnat_projectParticipant table1 ON xnat_subjectData.id=table1.subject_id) SECURITY WHERE ((((xnat_subjectData4=(%s)) AND  (xnat_subjectData6=(%s)))) AND ((((xnat_projectParticipant11='*') OR  ( (xnat_subjectData4 IS NOT NULL)))) OR (((xnat_subjectData4=(%s)) OR  (xnat_projectParticipant11=(%s))))))) SECURITY LEFT JOIN xnat_subjectData SEARCH ON SECURITY.xnat_subjectData3=SEARCH.id) xnat_subjectData   LEFT JOIN xnat_investigatorData table1 ON xnat_subjectData.investigator_xnat_investigatordata_id=table1.xnat_investigatordata_id   LEFT JOIN xnat_investigatorData_meta_data table2 ON table1.investigatorData_info=table2.meta_data_id   LEFT JOIN xnat_abstractDemographicData table3 ON xnat_subjectData.demographics_xnat_abstractdemographicdata_id=table3.xnat_abstractdemographicdata_id   LEFT JOIN xdat_meta_element table4 ON table3.extension=table4.xdat_meta_element_id   LEFT JOIN xnat_abstractDemographicData_meta_data table5 ON table3.abstractDemographicData_info=table5.meta_data_id   LEFT JOIN xnat_abstractSubjectMetadata table6 ON xnat_subjectData.metadata_xnat_abstractsubjectmetadata_id=table6.xnat_abstractsubjectmetadata_id   LEFT JOIN xdat_meta_element table7 ON table6.extension=table7.xdat_meta_element_id   LEFT JOIN xnat_abstractSubjectMetadata_meta_data table8 ON table6.abstractSubjectMetadata_info=table8.meta_data_id   LEFT JOIN xnat_subjectData_meta_data table9 ON xnat_subjectData.subjectData_info=table9.meta_data_id"""

 cursor.execute(cmd, (project_id, subject_label, project_id, project_id,))
 result = cursor.fetchall()
 if result:
     return True
 else:
     return False

def get_distinct_subject_ids(cursor):
 """
 Method to get all of the <XNAT_INSTANCE_NAME>_S%%%%%%% IDs.
  This query should ideally sort them based on the method to get the max ID.
 :param cursor:
 :return: tuple of XNAT subject IDs
 """
 cmd = """SELECT DISTINCT id FROM (SELECT id FROM xnat_subjectData WHERE id LIKE 'DEV_VUIISXNAT_S%' UNION SELECT DISTINCT id FROM xnat_subjectData_history WHERE id LIKE 'DEV_VUIISXNAT_S%') SRCH"""
 cursor.execute(cmd)
 result = cursor.fetchall()
 return result

def get_next_subject_id(subject_ids):
 """
 These IDs should really be some sort of serial8 or something of the like,
  but this sorts the tuple to get the max value and then adds
 :param cursor:
 :param subject_ids:
 :return: the new ID (in a tuple)
 """

 # Sort here rather than using postgres to mimic XNAT
 subject_ids.sort()
 last_id = subject_ids[len(subject_ids)-1]

 # I don't know if numbers are OK in the XNAT instance name. Thus, split the
 #  '_' and take the last element
 tail_of_id = last_id[0].split('_')
 last_id_digits = re.findall(r'\d+', tail_of_id[len(tail_of_id)-1])

 # pop the last element of the tail_of_id to reconstruct the XNAT instance name
 tail_of_id.pop(len(tail_of_id)-1)

 # I don't know if the zeropadding is a hard limit. This mimics the current install
 id = "%s_%05d" % ('_'.join(tail_of_id), int(last_id_digits[0])+1)
 return (id,)

def check_if_subject_id_exists(cursor, subject_id):
 """

 :param cursor:
 :param subject_id:
 :return:
 """
 cmd = """SELECT xnat_subjectData.id AS xnat_subjectData3, xnat_subjectData.investigator_xnat_investigatordata_id AS xnat_subjectData0, xnat_subjectData.demographics_xnat_abstractdemographicdata_id AS xnat_subjectData1, xnat_subjectData.metadata_xnat_abstractsubjectmetadata_id AS xnat_subjectData2, xnat_subjectData.project AS xnat_subjectData4, xnat_subjectData._group AS xnat_subjectData5, xnat_subjectData.label AS xnat_subjectData6, xnat_subjectData.src AS xnat_subjectData7, xnat_subjectData.initials AS xnat_subjectData8, xnat_subjectData.subjectdata_info AS xnat_subjectData9, table1.title AS xnat_investigatorData67, table1.firstname AS xnat_investigatorData68, table1.lastname AS xnat_investigatorData69, table1.institution AS xnat_investigatorData70, table1.department AS xnat_investigatorData71, table1.email AS xnat_investigatorData72, table1.phone AS xnat_investigatorData73, table1.id AS xnat_investigatorData74, table1.investigatordata_info AS xnat_investigatorData75, table1.xnat_investigatordata_id AS xnat_investigatorData76, table2.xft_version AS xnat_investigatorData_meta_data77, table2.last_modified AS xnat_investigatorData_meta_data78, table2.status AS xnat_investigatorData_meta_data79, table2.activation_date AS xnat_investigatorData_meta_data80, table2.row_last_modified AS xnat_investigatorData_meta_data81, table2.insert_date AS xnat_investigatorData_meta_data82, table2.activation_user_xdat_user_id AS xnat_investigatorData_meta_data83, table2.insert_user_xdat_user_id AS xnat_investigatorData_meta_data84, table2.origin AS xnat_investigatorData_meta_data85, table2.modified AS xnat_investigatorData_meta_data86, table2.shareable AS xnat_investigatorData_meta_data87, table2.meta_data_id AS xnat_investigatorData_meta_data88, table3.extension AS xnat_abstractDemographicData89, table3.abstractdemographicdata_info AS xnat_abstractDemographicData90, table3.xnat_abstractdemographicdata_id AS xnat_abstractDemographicData91, table4.element_name AS xdat_meta_element92, table4.xdat_meta_element_id AS xdat_meta_element93, table5.xft_version AS xnat_abstractDemographicData_meta_data94, table5.last_modified AS xnat_abstractDemographicData_meta_data95, table5.status AS xnat_abstractDemographicData_meta_data96, table5.activation_date AS xnat_abstractDemographicData_meta_data97, table5.row_last_modified AS xnat_abstractDemographicData_meta_data98, table5.insert_date AS xnat_abstractDemographicData_meta_data99, table5.activation_user_xdat_user_id AS xnat_abstractDemographicData_meta_data100, table5.insert_user_xdat_user_id AS xnat_abstractDemographicData_meta_data101, table5.origin AS xnat_abstractDemographicData_meta_data102, table5.modified AS xnat_abstractDemographicData_meta_data103, table5.shareable AS xnat_abstractDemographicData_meta_data104, table5.meta_data_id AS xnat_abstractDemographicData_meta_data105, table6.extension AS xnat_abstractSubjectMetadata106, table6.abstractsubjectmetadata_info AS xnat_abstractSubjectMetadata107, table6.xnat_abstractsubjectmetadata_id AS xnat_abstractSubjectMetadata108, table7.element_name AS xdat_meta_element109, table7.xdat_meta_element_id AS xdat_meta_element110, table8.xft_version AS xnat_abstractSubjectMetadata_meta_data111, table8.last_modified AS xnat_abstractSubjectMetadata_meta_data112, table8.status AS xnat_abstractSubjectMetadata_meta_data113, table8.activation_date AS xnat_abstractSubjectMetadata_meta_data114, table8.row_last_modified AS xnat_abstractSubjectMetadata_meta_data115, table8.insert_date AS xnat_abstractSubjectMetadata_meta_data116, table8.activation_user_xdat_user_id AS xnat_abstractSubjectMetadata_meta_data117, table8.insert_user_xdat_user_id AS xnat_abstractSubjectMetadata_meta_data118, table8.origin AS xnat_abstractSubjectMetadata_meta_data119, table8.modified AS xnat_abstractSubjectMetadata_meta_data120, table8.shareable AS xnat_abstractSubjectMetadata_meta_data121, table8.meta_data_id AS xnat_abstractSubjectMetadata_meta_data122, table9.xft_version AS xnat_subjectData_meta_data323, table9.last_modified AS xnat_subjectData_meta_data324, table9.status AS xnat_subjectData_meta_data325, table9.activation_date AS xnat_subjectData_meta_data326, table9.row_last_modified AS xnat_subjectData_meta_data327, table9.insert_date AS xnat_subjectData_meta_data328, table9.activation_user_xdat_user_id AS xnat_subjectData_meta_data329, table9.insert_user_xdat_user_id AS xnat_subjectData_meta_data330, table9.origin AS xnat_subjectData_meta_data331, table9.modified AS xnat_subjectData_meta_data332, table9.shareable AS xnat_subjectData_meta_data333, table9.meta_data_id AS xnat_subjectData_meta_data334 FROM (SELECT SEARCH.* FROM (SELECT DISTINCT ON (xnat_subjectData3) * FROM (SELECT xnat_subjectData.id AS xnat_subjectData3 FROM xnat_subjectData xnat_subjectData) SECURITY WHERE
 (
 ( (xnat_subjectData3=(%s))) AND
 ( (xnat_subjectData3=(%s))))) SECURITY LEFT JOIN xnat_subjectData SEARCH ON SECURITY.xnat_subjectData3=SEARCH.id) xnat_subjectData   LEFT JOIN xnat_investigatorData table1 ON xnat_subjectData.investigator_xnat_investigatordata_id=table1.xnat_investigatordata_id   LEFT JOIN xnat_investigatorData_meta_data table2 ON table1.investigatorData_info=table2.meta_data_id   LEFT JOIN xnat_abstractDemographicData table3 ON xnat_subjectData.demographics_xnat_abstractdemographicdata_id=table3.xnat_abstractdemographicdata_id   LEFT JOIN xdat_meta_element table4 ON table3.extension=table4.xdat_meta_element_id   LEFT JOIN xnat_abstractDemographicData_meta_data table5 ON table3.abstractDemographicData_info=table5.meta_data_id   LEFT JOIN xnat_abstractSubjectMetadata table6 ON xnat_subjectData.metadata_xnat_abstractsubjectmetadata_id=table6.xnat_abstractsubjectmetadata_id   LEFT JOIN xdat_meta_element table7 ON table6.extension=table7.xdat_meta_element_id   LEFT JOIN xnat_abstractSubjectMetadata_meta_data table8 ON table6.abstractSubjectMetadata_info=table8.meta_data_id   LEFT JOIN xnat_subjectData_meta_data table9 ON xnat_subjectData.subjectData_info=table9.meta_data_id"""
 cursor.execute(cmd, (subject_id, subject_id))
 result = cursor.fetchall()
 if result:
     return True
 else:
     return False

def get_next_wrk_wrkflowdata_id(cursor):
 """
 Get the next wrk_wrkflowData ID
 :param cursor:
 :return:
 """
 cmd = """SELECT nextval('public.wrk_workflowdata_wrk_workflowdata_id_seq') AS wrk_workflowData_id"""
 cursor.execute(cmd)
 result = cursor.fetchall()
 return result[0]

def select_i_wrk_workflowdata(cursor, wrkflowdata_id):
 """

 :param cursor:
 :param wrkflowdata_id:
 :return:
 """
 cmd = """SELECT i_wrk_workflowData((%s),0,FALSE,TRUE,false)"""
 cursor.execute(cmd, wrkflowdata_id)
 result = cursor.fetchall()

def check_if_wrk_workflowdata_exists(cursor, subject_id):
 """

 :param cursor:
 :param subject_id:
 :return:
 """
 timestamp = get_timestamp()
 cmd = """SELECT wrk_workflowData.wrk_workflowdata_id AS wrk_workflowData22, wrk_workflowData.executionenvironment_wrk_abstractexecutionenvironment_id AS wrk_workflowData0, wrk_workflowData.comments AS wrk_workflowData1, wrk_workflowData.details AS wrk_workflowData2, wrk_workflowData.justification AS wrk_workflowData3, wrk_workflowData.description AS wrk_workflowData4, wrk_workflowData.src AS wrk_workflowData5, wrk_workflowData.type AS wrk_workflowData6, wrk_workflowData.category AS wrk_workflowData7, wrk_workflowData.data_type AS wrk_workflowData8, wrk_workflowData.id AS wrk_workflowData9, wrk_workflowData.externalid AS wrk_workflowData10, wrk_workflowData.current_step_launch_time AS wrk_workflowData11, wrk_workflowData.current_step_id AS wrk_workflowData12, wrk_workflowData.status AS wrk_workflowData13, wrk_workflowData.create_user AS wrk_workflowData14, wrk_workflowData.pipeline_name AS wrk_workflowData15, wrk_workflowData.next_step_id AS wrk_workflowData16, wrk_workflowData.step_description AS wrk_workflowData17, wrk_workflowData.launch_time AS wrk_workflowData18, wrk_workflowData.percentagecomplete AS wrk_workflowData19, wrk_workflowData.jobid AS wrk_workflowData20, wrk_workflowData.workflowdata_info AS wrk_workflowData21, table1.extension AS wrk_abstractExecutionEnvironment23, table1.abstractexecutionenvironment_info AS wrk_abstractExecutionEnvironment24, table1.wrk_abstractexecutionenvironment_id AS wrk_abstractExecutionEnvironment25, table2.element_name AS xdat_meta_element26, table2.xdat_meta_element_id AS xdat_meta_element27, table3.xft_version AS wrk_abstractExecutionEnvironment_meta_data28, table3.last_modified AS wrk_abstractExecutionEnvironment_meta_data29, table3.status AS wrk_abstractExecutionEnvironment_meta_data30, table3.activation_date AS wrk_abstractExecutionEnvironment_meta_data31, table3.row_last_modified AS wrk_abstractExecutionEnvironment_meta_data32, table3.insert_date AS wrk_abstractExecutionEnvironment_meta_data33, table3.activation_user_xdat_user_id AS wrk_abstractExecutionEnvironment_meta_data34, table3.insert_user_xdat_user_id AS wrk_abstractExecutionEnvironment_meta_data35, table3.origin AS wrk_abstractExecutionEnvironment_meta_data36, table3.modified AS wrk_abstractExecutionEnvironment_meta_data37, table3.shareable AS wrk_abstractExecutionEnvironment_meta_data38, table3.meta_data_id AS wrk_abstractExecutionEnvironment_meta_data39, table4.xft_version AS wrk_workflowData_meta_data40, table4.last_modified AS wrk_workflowData_meta_data41, table4.status AS wrk_workflowData_meta_data42, table4.activation_date AS wrk_workflowData_meta_data43, table4.row_last_modified AS wrk_workflowData_meta_data44, table4.insert_date AS wrk_workflowData_meta_data45, table4.activation_user_xdat_user_id AS wrk_workflowData_meta_data46, table4.insert_user_xdat_user_id AS wrk_workflowData_meta_data47, table4.origin AS wrk_workflowData_meta_data48, table4.modified AS wrk_workflowData_meta_data49, table4.shareable AS wrk_workflowData_meta_data50, table4.meta_data_id AS wrk_workflowData_meta_data51 FROM (SELECT SEARCH.* FROM (SELECT DISTINCT ON (wrk_workflowData22) * FROM (SELECT wrk_workflowData.wrk_workflowdata_id AS wrk_workflowData22, wrk_workflowData.id AS wrk_workflowData9, wrk_workflowData.pipeline_name AS wrk_workflowData15, wrk_workflowData.launch_time AS wrk_workflowData18 FROM wrk_workflowData wrk_workflowData) SECURITY WHERE
 (
 (
 (
 ( (wrk_workflowData9=(%s)) AND  (wrk_workflowData15='Added Subject') AND  (wrk_workflowData18=(%s))))) AND
 (
 (
 ( (wrk_workflowData9=(%s)) AND  (wrk_workflowData15='Added Subject') AND  (wrk_workflowData18=(%s))))))) SECURITY LEFT JOIN wrk_workflowData SEARCH ON SECURITY.wrk_workflowData22=SEARCH.wrk_workflowdata_id) wrk_workflowData   LEFT JOIN wrk_abstractExecutionEnvironment table1 ON wrk_workflowData.executionenvironment_wrk_abstractexecutionenvironment_id=table1.wrk_abstractexecutionenvironment_id   LEFT JOIN xdat_meta_element table2 ON table1.extension=table2.xdat_meta_element_id   LEFT JOIN wrk_abstractExecutionEnvironment_meta_data table3 ON table1.abstractExecutionEnvironment_info=table3.meta_data_id   LEFT JOIN wrk_workflowData_meta_data table4 ON wrk_workflowData.workflowData_info=table4.meta_data_id"""
 cursor.execute(cmd, (subject_id,timestamp,subject_id,timestamp))
 result = cursor.fetchall()
 return result[0], timestamp

def get_next_xdat_change_info_id(cursor):
 """

 :param cursor:
 :return:
 """
 cmd = """SELECT nextval('public.xdat_change_info_xdat_change_info_id_seq') AS xdat_change_info_id"""
 cursor.execute(cmd)
 result = cursor.fetchone()
 return result[0]


def get_next_meta_data_id(cursor):
 """

 :param cursor:
 :return:
 """
 cmd = """nextval('public.wrk_workflowdata_meta_data_meta_data_id_seq') AS meta_data_id"""
 cursor.execute(cmd)
 result = cursor.fetchone()
 return result[0]

def insert_wrk_workflowdata_meta_data(cursor, insert_date, metadata_id):
 """

 :param cursor:
 :param insert_date: The date returned from check_if_wrk_workflowdata_exists
 :return:
 """
 cmd = """INSERT INTO wrk_workflowData_meta_data (xft_version,status,activation_user_xdat_user_id,activation_date,row_last_modified,insert_date,modified,insert_user_xdat_user_id,meta_data_id,shareable) VALUES ('125','active',1,(%s),(%s),(%s),0,1,(%d),1)"""
 timestamp = get_timestamp()
 cursor.execute(cmd,(timestamp, insert_date, insert_date, metadata_id))
 result = cursor.fetchall()
 return result, timestamp

def insert_wrk_workflowdata(cursor, workflow_info, workflow_id, subject_id, project_id, create_date):
 """

 :param cursor:
 :param workflow_info:
 :param workflow_id:
 :param subject_id:
 :param project_id:
 :param create_date:
 :return:
 """
 cmd = """INSERT INTO wrk_workflowData (workflowdata_info,wrk_workflowdata_id,id,category,pipeline_name,externalid,status,type,data_type,launch_time) VALUES ((%d),(%d),(%s),'DATA','Added Subject',(%s),'In Progress','WEB_FORM','xnat:subjectData',(%s)"""
 cursor.execute(cmd,(workflow_info, workflow_id, subject_id, project_id, create_date))
 cursor.commit()

def update_xdate_change_info(cursor, modified_date, metadata_id):
 """

 :param cursor:
 :param modified_date:
 :param metadata_id:
 :return:
 """
 cmd = """UPDATE wrk_workflowData_meta_data SET last_modified='(%s)', modified=1 WHERE meta_data_id=1(%d)"""
 cursor.execute(cmd, (modified_date, metadata_id))
 cursor.commit()

def insert_xdat_change_info(cursor, change_date, event_id):
 """

 :param cursor:
 :param change_date:
 :param event_id:
 :return:
 """
 cmd = """INSERT INTO xdat_change_info (xdat_change_info_id,change_user,change_date,event_id) VALUES (125,1,'(%s),(%d))"""
 cursor.execute(cmd, (change_date, event_id))
 cursor.commit()


def get_timestamp():
 """
 :return: timestamp
 """
 return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]