#!/usr/bin/env python
import rospy
from numpy import *
from std_msgs.msg import Float32

iX = 0
iY = 0
iZ = 0
dataX = [[0 for x in range(2)] for y in range(40)]
dataY = [[0 for x in range(2)] for y in range(40)]
dataZ = [[0 for x in range(2)] for y in range(40)]

def callbackX(msgX):
	global dataX
	global iX
	if iX < 40:
		dataX[iX][1] = msgX.data
		print(dataX[iX][1])
		iX += 1

def callbackY(msgY):
	global dataY
	global iY
	if iY < 40:
		dataY[iY][1] = msgY.data
		print(dataX[iY][1])
		iY += 1

def callbackZ(msgZ):
	global dataZ
	global iZ
	if iZ < 40:
		dataZ[iZ][1] = msgZ.data
		print(dataZ[iZ][1])
		iZ += 1

def listener():
	global iX
	rospy.init_node('accel_data_recorder', anonymous=True)

	rospy.Subscriber("accelX", Float32, callbackX)
	#rospy.Subscriber("accelY_recorder", accelY, callbackY)
	#rospy.Subscriber("accelZ_recorder", accelZ, callbackZ)
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()



def menu():
	global dataX 
	global dataY 
	global dataZ
	sum = 0
	i = 0
	j = 0
	while i < 40:
		dataX[i][j] = sum
		dataY[i][j] = sum
		dataZ[i][j] = sum
		sum = sum + 0.25
		i+=1
	check = 0
	while check != 1:
		check = input("Enter 1 when you are ready: ")
	listener()

if __name__ == '__main__':
	menu()