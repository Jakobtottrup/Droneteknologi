#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2020 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

##### Insert initialize code below ###################

## Uncomment the file to read ##
#fileName = 'imu_razor_data_static.txt'
fileName = 'imu_razor_data_pitch_55deg.txt'
#fileName = 'imu_razor_data_roll_65deg.txt'
#fileName = 'imu_razor_data_yaw_90deg.txt'

## IMU type
#imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

## Variables for plotting ##
showPlot = True
plotData = []
cleanData = []

## Initialize your variables here ##
myValue = 0.0

focus = []
def lowpass(p, t, w):
        focus.append(p)
        if len(focus) > t:
                focus.pop(0)
        focusMean = np.mean(focus)

        betterFocus = []
        index = 0
        for p in focus:
                if index >= len(focus) - 1:
                        betterFocus.append(p)
                if abs(p - focusMean) / focusMean < w:
                        betterFocus.append(p)
                index += 1
        betterMean = np.mean(betterFocus)
        
        return betterMean

######################################################

# import libraries
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt
import numpy as np

# open the imu data file
f = open (fileName, "r")

# initialize variables
count = 0

# looping through file

for line in f:
	count += 1

	# split the line into CSV formatted data
	line = line.replace ('*',',') # make the checkum another csv value
	csv = line.split(',')

	# keep track of the timestamps 
	ts_recv = float(csv[0])
	if count == 1: 
		ts_now = ts_recv # only the first time
	ts_prev = ts_now
	ts_now = ts_recv

	if imuType == 'sparkfun_razor':
		# import data from a SparkFun Razor IMU (SDU firmware)
		acc_x = int(csv[2]) / 1000.0 * 4 * 9.82;
		acc_y = int(csv[3]) / 1000.0 * 4 * 9.82;
		acc_z = int(csv[4]) / 1000.0 * 4 * 9.82;
		gyro_x = int(csv[5]) * 1/14.375 * pi/180.0;
		gyro_y = int(csv[6]) * 1/14.375 * pi/180.0;
		gyro_z = int(csv[7]) * 1/14.375 * pi/180.0;

	elif imuType == 'vectornav_vn100':
		# import data from a VectorNav VN-100 configured to output $VNQMR
		acc_x = float(csv[9])
		acc_y = float(csv[10])
		acc_z = float(csv[11])
		gyro_x = float(csv[12])
		gyro_y = float(csv[13])
		gyro_z = float(csv[14])
	 		
	##### Insert loop code below #########################

	# Variables available
	# ----------------------------------------------------
	# count		Current number of updates		
	# ts_prev	Time stamp at the previous update
	# ts_now	Time stamp at this update
	# acc_x		Acceleration measured along the x axis
	# acc_y		Acceleration measured along the y axis
	# acc_z		Acceleration measured along the z axis
	# gyro_x	Angular velocity measured about the x axis
	# gyro_y	Angular velocity measured about the y axis
	# gyro_z	Angular velocity measured about the z axis

	## Insert your code here ##
	
        # Gp is accelerometer xyz

	# 3.2.1 pitch
	#pitch = atan2(acc_y, sqrt(pow(acc_x, 2) + pow(acc_z, 2)))

	# 3.2.2 roll
	#roll = atan2(-acc_x, acc_z)

	# 3.2.3 accelerometer noise
	pitch = atan2(acc_y, sqrt(pow(acc_x, 2) + pow(acc_z, 2)))
	roll = atan2(-acc_x, acc_z)
        
	pitch = pitch*180.0/pi
	plotData.append(pitch)
	cleanData.append(lowpass(pitch, 10, 1.2))

	######################################################

# closing the file
f.close()

# show the plot
if showPlot == True:
	plt.plot(plotData)
	plt.plot(cleanData)
	plt.legend(['raw pitch', 'lowpass T10 120%diff'])
	plt.savefig('imu_exercise_plot.png')
	plt.show()

