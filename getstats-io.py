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
#~/Documents/Tasks/getstats-io.py


#importing the right libraries
import glob
from influxdb.influxdb08 import InfluxDBClient, SeriesHelper
import platform


# InfluxDB connections settings
host = 'metrics01.internal.sanger.ac.uk'
port = 8086
user = 'lustre'
password = 'lustre'
dbname = 'lustre'

myclient = InfluxDBClient(host, port, user, password, dbname)

class LustreIOStats(SeriesHelper):
    class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = '{series_name}'
        # Defines all the fields in this time series.
        fields = ['series_name', 'hostname', 'disk', 'value' ]
        # Defines all the tags for the series.
        # tags = ['hostname']
        # Defines the number of data points to store prior to writing on the wire.
        bulk_size = 5
        # autocommit must be set to True when using bulk_size
        autocommit = True

#Looking for the files within this directory and outputing certain lines from it
hostname=platform.node()
for filename in glob.glob("/proc/diskstats"):
		#whilst we have the file open as read only and assigned to "procfile"
		with open(filename,'r') as procfile:
			#new variable splits the file name by a space.
			#with open('/tmp/testgetio.txt', 'a') as iostats:
				for line in procfile:
					#this is splitting the line and assigning a new variable
					fieldentry = line.split()
					#a new variable to split to extract the 3rd field from a line.
					ioname = fieldentry[2]
					if 'sd' in line:
						#this is writing to file, the name of the "sd line" plus the required fields
						#iostats.write(ioname + " number of reads is " + fieldentry[3]+"\n")
						LustreIOStats(series_name="IO_reads_completed", hostname=hostname, disk=ioname, value=int(fieldentry[3]))
						#iostats.write(ioname + " time spent reading is " + fieldentry[6]+"\n")
						LustreIOStats(series_name="IO_read_time", hostname=hostname, disk=ioname, value=int(fieldentry[6]))
						#iostats.write(ioname + " number of writes is " + fieldentry[7]+"\n")
						LustreIOStats(series_name="IO_writes_completed", hostname=hostname, disk=ioname, value=int(fieldentry[7]))
						#iostats.write(ioname + " time spent writing is " + fieldentry[10]+"\n")
						LustreIOStats(series_name="IO_write_time", hostname=hostname, disk=ioname, value=int(fieldentry[10]))
						#iostats.write("\n")
					

			
