__author__ = 'damons'
import assessor_create_util
import sys
"""
This taks a 2 column csv file. The first column should be the assessor label
and the second should be the xsitype. Due to variable insertion concers in
psycopg2, the map between xsitype and the associated table in postgres is
hardcoded. The method get_statement_from_xsitype can easily be extended
by updating the map to handle extra xsitypes.

"""
if __name__ == '__main__':

    # Get the connection to postgres and the cursor
    conn = assessor_create_util.get_connection(password='')
    cursor = assessor_create_util.get_cursor(conn)

    if len(sys.argv) != 2:
        sys.stderr.write('Error. must pass <csv_file>\n')
        sys.exit(1)
    csv_file = sys.argv[1]

    with open(csv_file,'r') as f:
        data = f.readlines()

    for line in data:

        assessor = line.split(',')[0]
        xsi_type = line.split(',')[1].strip()

        assessor_label = assessor
        project_id = assessor_label.split('-x-')[0]
        subject_label = assessor_label.split('-x-')[1]
        experiment_label = assessor_label.split('-x-')[2]
        proctype = assessor_label.split('-x-')[-1]
        print "START ASSESSOR %s" % assessor_label

        # Check that the project, subject, experiment, and assessor label exist
        if not assessor_create_util.check_if_project_exits(cursor, project_id):
            print "Project ID %s does not exist. Cannot create assessor %s" % (project_id, assessor_label)
            continue

        if not assessor_create_util.check_if_subject_exists(cursor,project_id,subject_label):
            print "Subject Label %s does not exist for Project ID %s. Cannot create assessor %s" % (subject_label, project_id, assessor_label)
            continue

        if not assessor_create_util.check_if_experiment_exists(cursor,project_id,experiment_label):
            print "Experiment Label %s does not exist for Project ID %s. Cannot create assessor %s" % (experiment_label, project_id, assessor_label)
            continue

        if assessor_create_util.check_if_assessor_exists(cursor,project_id,assessor_label):
            print "Assessor Label %s already exists for Project ID %s. Cannot create." % (assessor_label, project_id )
            continue

        if not assessor_create_util.check_if_xsitype_exists(cursor, xsi_type):
            print "xsitype %s does not exist. Cannot create." % xsi_type
            continue

        # By default set the procstatus to NEED_INPUTS so we can let dax_build handle the rest of the checking.
        procstatus='NEED_INPUTS'

        # Reserve a lot of the (metadata) ids
        experiment_id = assessor_create_util.get_next_experiment_id(cursor)
        xdat_change_info_id = assessor_create_util.get_xdat_change_info_id(cursor)
        xnat_experimentdata_meta_data_meta_data_id = assessor_create_util.get_experimentdata_meta_data_id(cursor)
        xnat_deriveddata_meta_data_id = assessor_create_util.get_deriveddata_meta_data_id(cursor)
        xnat_imageassessordata_meta_data_meta_data_id = assessor_create_util.get_imageassesordata_meta_data_id(cursor)
        proc_genprocdata_meta_data_meta_data_id = assessor_create_util.get_procgenprocdata_meta_data_id(cursor)

        # experimentdata
        assessor_create_util.insert_xnat_experimentdata_meta_data(conn,cursor,xdat_change_info_id,xnat_experimentdata_meta_data_meta_data_id)
        assessor_create_util.insert_xnat_experimentdata(conn, cursor, xnat_experimentdata_meta_data_meta_data_id, assessor_label, project_id, experiment_id)

        # deriveddata
        assessor_create_util.insert_xnat_deriveddata_meta_data(conn,cursor,xdat_change_info_id, xnat_deriveddata_meta_data_id)
        assessor_create_util.insert_xnat_deriveddata(conn, cursor, xnat_deriveddata_meta_data_id, experiment_id)

        # image assessordata
        session_id = assessor_create_util.get_experiment_id_from_label(cursor, project_id, experiment_label)
        assessor_create_util.insert_xnat_imageassessordata_meta_data(conn, cursor, xdat_change_info_id, xnat_imageassessordata_meta_data_meta_data_id)
        assessor_create_util.insert_xnat_imageassessordata(conn, cursor, xnat_imageassessordata_meta_data_meta_data_id, experiment_id, session_id[0])

        # finally, the assesor type
        assessor_create_util.insert_proc_genprocdata_meta_data(conn, cursor, xdat_change_info_id, proc_genprocdata_meta_data_meta_data_id)
        assessor_create_util.insert_proc_genprocdata(conn,cursor,proc_genprocdata_meta_data_meta_data_id,experiment_id)

        assessor_create_util.insert_need_inputs_status(conn,cursor,procstatus,proctype, experiment_id)
        print "FINISHED ASSESSOR %s" % assessor_label
