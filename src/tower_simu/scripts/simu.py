#!/usr/bin/env python3
import imp
import numpy as np
from torch import div
from genpy import Duration
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Quaternion,PoseStamped,PointStamped
from visualization_msgs.msg import Marker
from math import sin,cos,pi 
import time
theta = 0 #旋转角，0-2pi
r = 300 #旋转半径，单位毫米

def rpy2quaternion(roll, pitch, yaw):
    x=sin(pitch/2)*sin(yaw/2)*cos(roll/2)+cos(pitch/2)*cos(yaw/2)*sin(roll/2)
    y=sin(pitch/2)*cos(yaw/2)*cos(roll/2)+cos(pitch/2)*sin(yaw/2)*sin(roll/2)
    z=cos(pitch/2)*sin(yaw/2)*cos(roll/2)-sin(pitch/2)*cos(yaw/2)*sin(roll/2)
    w=cos(pitch/2)*cos(yaw/2)*cos(roll/2)-sin(pitch/2)*sin(yaw/2)*sin(roll/2)
    return x, y, z, w
if __name__ == "__main__":
    rospy.init_node('tower')
    pub = rospy.Publisher('armor',Marker,queue_size=1)
    ypub = rospy.Publisher('armor_x_position',Float32,queue_size=1)
    rate = rospy.Rate(100)
    h= rospy.Rate(1000)
    current_time = rospy.Time.now()
    last_time = rospy.Time.now()
    
    armors = []
    for i in range(3):
        armor = Marker()
        armor.ns = "basic_shapes"
        armor.id = i;
        armor.header.frame_id = "odom"
        armor.type = Marker.CUBE
        armor.action = Marker.ADD
        armors.append(armor)
    print("begin generating")
    t0 = time.time()
    divider = time.time()
    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        

        for i in range(3):
            armors[i].header.stamp = current_time
            armors[i].pose.position.x = r*cos(theta + i * (2/3)*pi)
            armors[i].pose.position.y = r*sin(theta + i * (2/3)*pi)
            armors[i].pose.position.z = 1
            yaw = theta + pi/2 + i * (2/3)*pi
            armors[i].pose.orientation.x, \
                armors[i].pose.orientation.y, \
                armors[i].pose.orientation.z, \
                armors[i].pose.orientation.w = rpy2quaternion(0,0,yaw)
            
            armors[i].scale.x = 200.0
            armors[i].scale.y = 50.0
            armors[i].scale.z = 100.0

            armors[i].color.r = 0
            armors[i].color.g = 0.5
            armors[i].color.b = 0
            armors[i].color.a = 1
            if yaw % (2*pi) > (1/4)*pi and yaw % (2*pi) < (3/4)*pi :
                armors[i].color.g = 0
                armors[i].color.r = 1
                if time.time() - divider > 0.007:
                    divider = time.time()
                    ypub.publish(armors[i].pose.position.y)
            armors[i].lifetime = rospy.Duration(1);
        if theta % (2*pi) < 0.025:
            print("T:",time.time() - t0)
            t0 = time.time()
        theta = theta + 0.025
        #这个麻烦的sleep折腾了我好久
        h.sleep()
        pub.publish(armors[0])
        h.sleep()
        pub.publish(armors[1])
        h.sleep()
        pub.publish(armors[2])
        # pub.publish(armors[3])
        rate.sleep()
