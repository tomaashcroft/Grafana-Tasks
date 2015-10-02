#!/bin/bash
""" Copyright (c) 2015, Genome Research Ltd
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of Grafana-Tasks nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

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
