#!/usr/bin/env python
import argparse
import sys
import copy
import rospy
import geometry_msgs.msg
import shape_msgs.msg
import numpy as np
from leap_motion.msg import leapros, Human, Hand, Bone, Finger
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Int32

#Publisher for deterimining where the index finger is along the z axis (the leap motion switches this around and it is actually the y axis in the msg)
pub = rospy.Publisher('texture_level',Float32,queue_size=1)
#Publisher for generating the pulse the user feels when the index finger scans across a peak
pub2 = rospy.Publisher('pulse',Int32,queue_size=1)

#The points at which there are peaks. Along the y axis (z axis for the leap motion) and is infinte length along the x axis.

r_m = range(-210, 185, 10)
wood = range(-200, 185, 30)
cloth = range(-200, 185, 25)
card = range(-210, 185, 15)
paper = r_m
texture = [r_m,wood,cloth,card,paper]

#0 = rubber mat
#1 = wood
#2 = cloth
#3 = cardboard
#4 = paper

#The peak frequency of the pulse. 
peak = [230, 230, 230, 200, 230]

#Values used to determine where the finger is currently between peaks.
min_peak = 0
max_peak = 0
rng_set = 0

#The absolute maximum range of the 
abs_max_peak = texture[0][-1]
abs_min_peak = texture[0][0]

t = 0 #index for which texture is present.

#function for determining where the peaks currently are. Moving past a peak triggers a pulse.
def datasort(human_msg):
        global rng_set, max_peak, min_peak, t, abs_max_peak, abs_min_peak
        #if the user's hand is present then begin to check position otherwise there will be a constant bad callback if the hand is not present
        if human_msg.right_hand.is_present == True:
            lm_index_pos = human_msg.right_hand.finger_list[1].bone_list[3].bone_end.position
            index_pos = np.array([lm_index_pos.x*1000, lm_index_pos.y*1000, lm_index_pos.z*1000])
            pub.publish(Float32(index_pos[1]))
            #if the user goes below the point where the object is then begin texture synthesis
            if index_pos[1] < 150:
                if rng_set == 0:
                    i = 0
                    for x in texture[t]:
                        if x < index_pos[2]:
                            min_peak = x
                            if i == len(texture[t]):
                                max_peak = texture[t][i]
                            else:
                                max_peak = texture[t][i+1]
                        i += 1
                    rng_set = 1
                    #print where the peaks ranges currently are
                    print(min_peak)
                    print(max_peak)
            #If the user goes past the peak ranges then a pulse is generated
                else:
                    if index_pos[2] > abs_max_peak or index_pos[2] < abs_min_peak:
                        rng_set = 0
                    elif index_pos[2] > max_peak or index_pos[2] < min_peak:
                        pub2.publish(Int32(peak[t]))
                        rng_set = 0
            else:
                rng_set = 0

def texture_select(t_msg):
    global t, abs_min_peak, abs_max_peak
    t = t_msg.data
    abs_min_peak = texture[t][0]
    abs_max_peak = texture[t][-1]
    pass

def leap_sub_pub():
    rospy.init_node('texture_node',anonymous = True)
    rospy.Subscriber("/leap_motion/leap_device", Human, datasort, queue_size=1) # Subscribe to the topic and call lm_move each time we receive some input
    rospy.Subscriber("/t_select", Int32, texture_select, queue_size = 1) # Selects which texture is ac"/leap_motion/leap_device"tive in RViz
    #rospy.Subscriber("/leapmotion/data", leapros, datasort, queue_size=1)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        leap_sub_pub()
    except rospy.ROSInterruptException:
        pass