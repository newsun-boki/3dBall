#!/usr/bin/env python3
import time
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float32
history_x = []
history_t = []

#由于rviz坐标系与相机坐标系，实际上我这里接受的虽然是y坐标，但在实际中x坐标
def Callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    history_x.append(data.data)
    history_t.append(time.time()-t0)
    if len(history_t) > 100:
        history_t.pop(0)
        history_x.pop(0) 
if __name__ == "__main__":
    rospy.init_node('drawer')
    plt.ion()  #打开交互模式
    sub = rospy.Subscriber("armor_x_position",Float32,Callback)
    t0 = time.time()
    while True:
        plt.figure(0)
        plt.title('x_position')
        plt.scatter(history_t,history_x)
        plt.show()
        plt.pause(0.0001)
        plt.clf()  #清除图像

    #rospy.spin()

