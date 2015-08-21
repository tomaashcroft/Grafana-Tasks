#!/bin/bash
#
# Script to monitor and tune lustre inode/dentry slabcache.
# 
# distributred via cfengine
#

DATABASE=/nfs/ssg_group/lustre-monitoring/rrds/${HOSTNAME}-slab.rrd

while [ 1 ] ; do

cache=`cat /proc/sys/vm/vfs_cache_pressure`

while read line ; do
    set -- $line
    case $1 in
	dentry*)
	    dobj=$3
	    dsize=$4
	;;
	ldiskfs_inode_cache*)
	    iobj=$3
	    isize=$4
    esac
done < <(cat /proc/slabinfo)

((dslab=$dobj*$dsize))
((islab=$iobj*$isize))


timestamp=`/bin/date +%s`
/usr/bin/rrdtool update $DATABASE $timestamp:$dslab:$islab:$cache


sleep 30
done
