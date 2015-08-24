#!/usr/bin/env python
# This script is looking for data within different lustre stats.

#importing the right libraries
import glob
#Looking for the files within this directory and outputing certain lines from it
for filename in glob.glob("/proc/diskstats"):
		#whilst we have the file open as read only and assigned to "procfile"
		with open(filename,'r') as procfile:
			#new variable splits the file name by a space.
			with open('/tmp/testgetio.txt', 'a') as iostats:
				for line in procfile:
					#this is splitting the line and assigning a new variable
					fieldentry = line.split()
					#a new variable to split to extract the 3rd field from a line.
					ioname = fieldentry[2]
					if 'sd' in line:
						#this is writing to file, the name of the "sd line" plus the required fields
						iostats.write(ioname + " readn is " + fieldentry[3]+"\n")
						iostats.write(ioname + " readt is " + fieldentry[6]+"\n")
						iostats.write(ioname + " writen is " + fieldentry[7]+"\n")
						iostats.write(ioname + " writet is " + fieldentry[10]+"\n")
						iostats.write("\n")
					
