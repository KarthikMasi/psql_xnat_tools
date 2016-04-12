__author__ = 'damons'

import subject_creation_util

if __name__ == '__main__':
    TEST_GOOD_ID='XXXXXXX'
    TEST_GOOD_PROJECT='TEST1'
    conn = subject_creation_util.get_connection()
    cursor = subject_creation_util.get_cursor(conn)
    subject_exists = subject_creation_util.check_if_subject_label_exists(cursor,TEST_GOOD_PROJECT,TEST_GOOD_ID)
    if subject_exists:
        print "SUBJECT EXITS"

    distinct_subject_ids = subject_creation_util.get_distinct_subject_ids(cursor)
    next_subject_id = subject_creation_util.get_next_subject_id(distinct_subject_ids)

    # Now what we have the ID, make sure that it doesn't exist
    id_exists = subject_creation_util.check_if_subject_id_exists(cursor,next_subject_id)
    if id_exists:
        print "ID EXISTS"
    subject_creation_util.get_next_wrk_wrkflowdata_id(cursor)
