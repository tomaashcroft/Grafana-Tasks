#!/software/bin/python-2.7.9
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
