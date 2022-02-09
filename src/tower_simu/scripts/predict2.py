#!/usr/bin/env python3
import time
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Quaternion,PoseStamped,PointStamped
import math
from tower_simu.msg import armor_position
t0 = time.time()
history_x = []
history_y = []
history_t = []
predict_p = [0,0]#xy
bullet_time = 0.3
#由于rviz坐标系与相机坐标系，实际上我这里接受的虽然是y坐标，但在实际中x坐标
def Callback(data):
    global predict_p
    ct = time.time() - t0
    # for i in range(len(history_t)):
    #     if abs(ct-history_t[i]-0.833) < 0.005:
    #         predict_p[0] = history_x[i]
    #         predict_p[1] = history_y[i]  
    #         break        
    #     predict_p = [0,0]
    history_x.append(data.y)
    history_t.append(ct)
    history_y.append(data.x)
    if len(history_t) > 200:
        history_t.pop(0)
        history_x.pop(0) 
        history_y.pop(0)
    

if __name__ == "__main__":
    rospy.init_node('drawer')
    sub = rospy.Subscriber("armor_p",armor_position,Callback)
    pub = rospy.Publisher('predict_p',PointStamped,queue_size=1)
    this_point_stamp = PointStamped()
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        ct = time.time() - t0
        for i in range(len(history_t)):
            if abs(ct-history_t[i]-(0.833-bullet_time)) < 0.005:
                predict_p[0] = history_x[i]
                predict_p[1] = history_y[i]  
                break        
            predict_p = [0,0]
        this_point_stamp.header.stamp = rospy.Time.now()
        this_point_stamp.header.frame_id = "odom"
        this_point_stamp.point.x = predict_p[1]
        this_point_stamp.point.y = predict_p[0]
        this_point_stamp.point.z = 1
        pub.publish(this_point_stamp)
        rate.sleep()
    rospy.spin()

