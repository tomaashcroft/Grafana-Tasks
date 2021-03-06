#!/software/bin/python-2.7.9
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
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# This script is looking for data within different lustre stats."""
# This script is looking for mds data within different lustre file systems.

# importing the right libraries
import glob
from influxdb.influxdb08 import InfluxDBClient, SeriesHelper
import platform
from subprocess import check_output, CalledProcessError, STDOUT
import sys
import os

# InfluxDB connections settings
host = 'metrics01.internal.sanger.ac.uk'
port = 8086
user = 'lustre'
password = 'lustre'
dbname = 'lustre'

myclient = InfluxDBClient(host, port, user, password, dbname)


class LustreMDSStats(SeriesHelper):
    class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets
        series_name = '{series_name}'
        # Defines all the fields in this time series.
        fields = ['series_name', 'hostname', 'disk', 'value']
        # Defines all the tags for the series.
        # tags = ['hostname']
        # Defines the number of data points to store prior to writing on the wire.
        bulk_size = 5
        # autocommit must be set to True when using bulk_size
        autocommit = True

hostname = platform.node()
# check_output('/usr/sbin/lctl list_param mdt.*.md_stats', shell=True)
if not os.path.isfile('/usr/sbin/lctl'):
    sys.exit(0)
try:
    lctl_output = check_output(['/usr/sbin/lctl', 'list_param', 'mdt.*.md_stats'], stderr=STDOUT)
except CalledProcessError as e:
    sys.exit(0)
statsfile = "/proc/fs/lustre/" + lctl_output.strip().replace('.', '/')
# print (statsfile)


def getprocstats(pathname):
    for filename in glob.glob(pathname):
        # Looking for the files within this directory and outputing certain lines from it
        with open(filename, 'r') as procfile:
            ostname = filename.split("/")[-2]
            for line in procfile:
                fieldentry = line.split()
                if 'getattr' in line:
                    LustreMDSStats(series_name="MDS_getattr", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'setattr' in line:
                    LustreMDSStats(series_name="MDS_setattr", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'statfs' in line:
                    LustreMDSStats(series_name="MDS_statsfs", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'getxattr' in line:
                    LustreMDSStats(series_name="MDS_getxattr", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'rename' in line:
                    LustreMDSStats(series_name="MDS_rename", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'rmdir' in line:
                    LustreMDSStats(series_name="MDS_rmdir", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'mkdir' in line:
                    LustreMDSStats(series_name="MDS_mkdir", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'unlink' in line:
                    LustreMDSStats(series_name="MDS_unlink", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'link' in line:
                    LustreMDSStats(series_name="MDS_link", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'close' in line:
                    LustreMDSStats(series_name="MDS_close", hostname=hostname, disk=ostname, value=int(fieldentry[1]))
                elif 'open' in line:
                    LustreMDSStats(series_name="MDS_open", hostname=hostname, disk=ostname, value=int(fieldentry[1]))


getprocstats("/proc/fs/lustre/mds/*MDT0000/stats")
getprocstats("/proc/fs/lustre/osc/*osc/stats")
getprocstats(statsfile)
