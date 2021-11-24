#!/usr/bin/env python3
import numpy as np
import cv2
import random as rd
import rospy
from geometry_msgs.msg import Quaternion,PoseStamped,PointStamped
height= 1080
width = 720

class Ball3D:
    def __init__(self):
        self.v = np.array([0,0,0],dtype=np.int64) #定义球的速度
        self.v_now = np.array([0,0,0],dtype=np.int64) #定义球的速度
        self.alpha = 0.005#速度系数
        self.p = np.array([5,5,0])
        l = []
        for i in range(50):#定义惯性系数
            l.append([rd.random(),rd.random(),rd.random()])
        self.past_vs = np.array(l,dtype=np.int64)
        
    def update_v(self):
        self.v_now[0] = (rd.random()-0.5) * 10#通过改变这三个系数改变它
        self.v_now[1] = (rd.random()-0.5) * 10
        self.v_now[2] = (rd.random()-0.3) * 10
        self.past_vs = np.roll(self.past_vs,1,axis = 0)
        
        self.past_vs[0] = self.v_now
        self.v = np.mean(self.past_vs,axis=0)

    def move(self):
        self.update_v()
        self.p = self.p + self.alpha * self.v    
    



if __name__ == "__main__":
    rospy.init_node('random_ball')
    pub = rospy.Publisher('position',PointStamped,queue_size=1)
    rate = rospy.Rate(500)
    ball = Ball3D()
    current_time = rospy.Time.now()
    last_time = rospy.Time.now()

    this_point_stamp = PointStamped()

    

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()

        this_point_stamp.header.stamp = current_time
        this_point_stamp.header.frame_id = "odom"
        this_point_stamp.point.x = ball.p[0]%10/5;
        this_point_stamp.point.y = ball.p[1]%10/5;
        this_point_stamp.point.z = ball.p[2]%10/5;
        rospy.loginfo('current_x: {:.4f}'.format(ball.p[0]%10/5))
        rospy.loginfo('current_y: {:.4f}'.format(ball.p[1]%10/5))
        rospy.loginfo('current_z: {:.4f}'.format(ball.p[2]%10/5))
        pub.publish(this_point_stamp)
        # background = np.zeros((width, height, 3), dtype = "uint8")
        # cv2.circle(background,(round(ball.p[0])%height,round(ball.p[1])%width),20,(0,0,255),-1)
        # cv2.imshow("a",background)
        ball.move()
        rate.sleep()
        # cv2.waitKey(10) 
