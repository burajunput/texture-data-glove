#!/usr/bin/env python
import argparse
import sys
import copy
import rospy
import geometry_msgs.msg
import shape_msgs.msg
import numpy as np



if __name__ == '__main__':
	r_m = range(-210, 185, 5)
	wood = range(-200, 185, 25)
	cloth = range(-200, 185, 20)
	card = range(-210, 185, 10)
	paper = r_m
	texture = [r_m,wood,cloth,card,paper]
	print texture[0][1]