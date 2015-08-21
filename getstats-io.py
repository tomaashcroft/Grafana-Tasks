#!/usr/bin/env python
# This script is looking for data within different lustre stats.

import glob
for filename in glob.glob("/proc/diskstats"):
		#Looking for the files within this directory and outputing certain lines from it
		with open(filename,'r') as procfile:
			ioname = filename.split(" ")[-2]
			with open('/tmp/testgetio.txt', 'a') as iostats:
				for line procfile:
					fieldentry = line.split()
					if 'read_bytes' in line:
						lusstats.write(ostname + " current read_calls are " + fieldentry[1]+"\n")
						lusstats.write(ostname + " current read_bytes are " + fieldentry[6]+"\n")
						lusstats.write("\n")
					elif 'write_bytes' in line:
						lusstats.write(ostname + " current write_calls are " + fieldentry[1]+"\n")
						lusstats.write(ostname + " current write_bytes are " + fieldentry[6]+"\n")
						lusstats.write("\n")
					elif 'cache_access' in line:
						print(line)
					elif 'cache_hit' in line:
						print(line)
					elif 'cache_miss' in line:
						print(line)
			
