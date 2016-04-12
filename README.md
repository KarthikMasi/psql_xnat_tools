# psql_xnat_tools
A repo of XNAT tools that use pyscopg2 rather than PyXNAT to do a lot of the "heavy lifting" such as multiple set methods. PyXNAT is still used to get bulk information (e.g. All Assessors for a project, all sessions for a project etc).

These tools should only be used by XNAT admins as they expose a direct connection to the database. 
