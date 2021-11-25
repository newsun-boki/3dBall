#!/usr/bin/env python3
import numpy as np
import random as rd
import rospy
from geometry_msgs.msg import Quaternion,PoseStamped,PointStamped

class Ball3D:
    def __init__(self):
        
        self.v_now = np.array([0,0,0],dtype=np.int64) #定义球的速度
        self.alpha = 0.2#速度系数
        self.v = np.array([0,0,0],dtype=np.int64) #定义球的速度
        self.p = np.array([5,5,0])#位置
        self.a = np.array([0,0,0])#加速度
        self.a_now = np.array([0,0,0])

        l = []
        for i in range(8000):#定义惯性系数
            l.append([rd.random(),rd.random(),rd.random()])
        self.past_vs = np.array(l,dtype=np.int64)
        self.past_as = np.array(l,dtype=np.int64)
        
    def update_v(self):
        self.v_now[0] = (rd.random()-0.5) * 10#通过改变这三个系数改变它
        self.v_now[1] = (rd.random()-0.5) * 10
        self.v_now[2] = (rd.random()-0.5) * 10
        self.past_vs = np.roll(self.past_vs,1,axis = 0)
         
        self.past_vs[0] = self.v_now

        self.v = np.mean(self.past_vs,axis=0)#均值滤波
        cmp_tmp = self.p + self.alpha * self.v
        for i in range(3):#碰撞检测
            if cmp_tmp[i] > 10 or cmp_tmp[i] < 0 :
                self.past_vs[:,i] = self.past_vs[:,i]*(-1)
                self.v = self.v* (-1)
    #没用到的函数，一开始本来想用加速度的模式，但似乎小球运动不够随机
    def update_a(self):
        self.a_now[0] = (rd.random()-0.5) * 10#通过改变这三个系数改变它
        self.a_now[1] = (rd.random()-0.5) * 10
        self.a_now[2] = (rd.random()-0.5) * 10
        
        self.past_as =np.roll(self.past_as,1,axis = 0)
        self.past_as[0] = self.a_now
        self.a = np.mean(self.past_as,axis=0)
        self.v = self.a*0.001 + self.v
        cmp_tmp = self.p + self.alpha * self.v
        for i in range(3):
            if cmp_tmp[i] > 10 or cmp_tmp[i] < 0 :
                self.past_as[:,i] = self.past_as[:,i]*(-1)
                self.a = self.a* (-1)
                self.v = self.v* (-1)
    #小球云顶
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
        this_point_stamp.point.x = ball.p[0]%10/5
        this_point_stamp.point.y = ball.p[1]%10/5
        this_point_stamp.point.z = ball.p[2]%10/5
        rospy.loginfo('current_x: {:.4f}'.format(ball.p[0]%10/5))
        rospy.loginfo('current_y: {:.4f}'.format(ball.p[1]%10/5))
        rospy.loginfo('current_z: {:.4f}'.format(ball.p[2]%10/5))
        pub.publish(this_point_stamp)
        
        ball.move()
        rate.sleep()
