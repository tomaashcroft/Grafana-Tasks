#!/bin/bash
# Gets disk stats and plonk them into rrdtool.


# Location of the database
DATABASE=/nfs/ssg_data01/lustre_users/${HOSTNAME}


while [ 1  ] ; do 
/opt/lustre-monitor/lustre_ost_stats > $DATABASE
sleep 180
done
