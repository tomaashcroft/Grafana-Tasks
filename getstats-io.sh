#!/bin/bash
# Gets disk stats and plonk them into rrdtool.
# 
# distributred via cfengine
#


# Location of the database
DATABASE=/nfs/ssg_group/lustre-monitoring/rrds/${HOSTNAME}io.rrd


while [ 1  ] ; do 

readn=0
writen=0
readt=0
writet=0


# read stats
while read line ; do
set -- $line

((readn=$readn+$4))
((readt=$readt+$7))
((writen=$writen+$8))
((writet=$writet+${11}))


done < <(cat  /proc/diskstats | grep sd)

timestamp=`/bin/date +%s`
/usr/bin/rrdtool update $DATABASE $timestamp:$readn:$writen:$readt:$writet

sleep 30
done
