#!/bin/bash
# Gets MDS stats and plonk them into rrdtool.
# 
# distributred via cfengine
#

# Location of the database
DATABASE=/nfs/ssg_group/lustre-monitoring/rrds/$HOSTNAME.rrd

# lustre 1.8.X and 2.X keep stats in different places:

v1statsfile=`/usr/sbin/lctl list_param mds.*.stats 2> /dev/null | sed  's/\./\//g'`
v2statsfile=`/usr/sbin/lctl list_param mdt.*.md_stats 2> /dev/null | sed  's/\./\//g'`

if [[ -z $v2statsfile ]] ; then
datafile=/proc/fs/lustre/$v1statsfile
else
datafile=/proc/fs/lustre/$v2statsfile
fi

# Init variables to rrdtools "unknown" values.

open=U
close=U
link=U
unlink=U
mkdir=U
rmdir=U
rename=U
getxattr=U
statfs=U
setattr=U
getattr=U
create=U

# Read stats from /proc/fs/lustre/mds/*MDT0000/stats

while [ 1  ] ; do 

while read line ; do
set -- $line
    case $1 in
	open*)
	    open=$2;;
	close*)
	    close=$2;;
	link*)
	    link=$2;;
	unlink*)
	    unlink=$2;;
	mkdir*)
	    mkdir=$2;;
	rmdir*)
	    rmdir=$2;;
	rename*)
	    rename=$2;;
	getxattr*)
	    getxattr=$2;;
	statfs*)
	    statfs=$2;;
	setattr*)
	    setattr=$2;;
	getattr*)
	    getattr=$2;;
    esac
done < <(cat $datafile)


create=0
while read line ; do
set -- $line
((create=$create+$2))
done < <(cat /proc/fs/lustre/osc/*osc/stats | grep ost_create)

# If create=0 then no create counters were set; set to undefined.
if [ $create == 0 ] ; then
create=U
fi

timestamp=`/bin/date +%s`

/usr/bin/rrdtool update $DATABASE $timestamp:$open:$close:$link:$unlink:$mkdir:$rmdir:$rename:$getxattr:$statfs:$setattr:$getattr:$create

sleep 30
done
