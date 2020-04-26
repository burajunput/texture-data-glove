#!/usr/bin/env python
import argparse
import sys
import copy
import rospy
import numpy as np
from std_msgs.msg import Int32

pub = rospy.Publisher('peak', Int32, queue_size = 1)

def talker():
	rospy.init_node('talker', anonymous = True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		msg = raw_input('Peak?: ')
		pub.publish(1)
		rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass