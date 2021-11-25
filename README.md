<!--
 * @Author: your name
 * @Date: 2021-11-24 15:29:53
 * @LastEditTime: 2021-11-25 14:28:21
 * @LastEditors: newsun-HP-Pavilion-Gaming-Laptop-15-dk0xxx
 * @Description: In User Settings Edit
 * @FilePath: /rmtrain_ws/README.md
-->
# 视觉进阶培训1-运动预测

三维弹球，准确的来说有点像气体分子的运动，可以看成空间中有一个小球（无重力），以随机的速度在空间中游动，碰到边缘会反弹，而你要做的就是预测小球一定时间之后的位置。

## 依赖
  
+ numpy 1.20
  
+ ros melodic

+ Eigen 
## 快速开始


```bash
git clone https://github.com/newsun-boki/3dBall.git
cd 3dBall
catkin_make # rm -rf ./build ./devel if exits
source devel/setup.bash #记得每打开一个终端都要source一下
```
```bash
roscore

rosrun random_ball simu.py #用于生成小球

rosrun random_ball basic_shapes #用于生成绿色框

rviz -d src/random_ball/rm.rviz #在rviz中显示
```


![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/ball.6tt9rynnjeo0.gif)


## 任务说明

### 必要知识

+ c++/python基础知识
+ 了解ros的topic机制
+ 了解rviz的使用
+ 卡尔曼滤波(KF)或扩展卡尔曼滤波(EKF)或抗差卡尔曼滤波(UKF)
### 任务简介

已知小球小球当前时刻的三维坐标，预测小球一定时间之后所处的位置(反弹部分不作要求)。节点图如下。
![节点图](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/Screenshot-from-2021-11-25-13-22-34.1hdjhcrer068.png)
+ 节点`/basic_shapes`用于发布`/visualization_marker`话题，即绿色边界框。
+ 节点`/random_ball`用于发布`/position`话题，即小球的位置。
### 步骤

#### 获取小球当前位置。
+ 当运行`rosrun random_ball simu.py`后，通过`rostopic list`可以查询到有小球当前位置话题`/position`。
![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/Screenshot-from-2021-11-25-13-27-19.10uiu20b9brk.png)
+ 发送内容为
![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/Screenshot-from-2021-11-25-13-29-11.1lyv1ga20kio.png)
+ 发送的消息格式为`geometry_msgs/PointStamped`，关于数据格式的了解见roswiki。
![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/Screenshot-from-2021-11-25-13-34-34.75bszbno3iw0.png)
+ 发送频率大概是450hz
![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/Screenshot-from-2021-11-25-13-28-44.6s1gt3r2c3w0.png)

这里需要重新写一个**预测节点**，并在节点内创建一个`Subscriber`用于订阅`/position`话题。
#### 预测
使用各种卡尔曼滤波(如EKF)的手段进行**预测**。通过小球之前的位置预测小球一段时间之后的位置，具体预测多久可自行决定。这里需要你学习一些卡尔曼的相关知识，使用Eigen库辅助来完成一些数学运算，尽量不要使用opencv自带的卡尔曼滤波。推荐B站DR_CAN的卡尔曼滤波相关[讲解视频](https://www.bilibili.com/video/BV1ez4y1X7eR).但注意简单的卡尔曼是线性的，所以需要用一些如扩展卡尔曼等。
![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211125/Screenshot-from-2021-11-25-14-19-03.49vp6ibwwqm0.png)


#### RVIZ显示
这里你需要大概了解rviz的使用方法。rviz可以接受话题里的消息并将其显示出来，你需要做的就是将你预测的结果发布为`PointStamped`格式并使用rviz显示，如果不了解结果可以参考`simu.py`里的实现。将**你的预测结果用换一个颜色的小球显示出来**就好。

## 备注

+ `rosrun random_ball simu.py`这个命令`ctrl+c`似乎停不下来，你可以使用`ctrl+z`将其挂到后台暂停它,然后通过`jobs`查看后台任务,并使用`kill %num`杀死它，`num`为其在`jobs`查看时任务对应的序号。
+ 由于物体是随机运动，所以预测一段之后的时间不能过长，当然也不能过短。至于是多少，你看着觉得多少合适就多少。
+ 评价预测好坏主要有两个指标
  +  **收敛速度**。包括当小球从静止到运动需要多久才能开始准确预测，以及当小球撞击边缘速度发生突变时尽量收敛到正确方向的时间(可以采取一些如当检测速度突变就reset卡尔曼的手段)
  +  **预测结果的稳定性**。在实际控制当中，为了使电机不震颤，视觉的预测结果需要尽量的平滑稳定，即预测点不要乱抖。
+ 如果你觉的这个弹球模型好玩，并且看懂了弹球代码，你可以编写`simu.py`程序自己往里面多加几个球并加上物理体积的碰撞。或者我一总觉得这个碰到边缘没有音效怪怪的，你可以自己往里面加点音效。
+ 为了方便查看，这个README我也会发到博客上。
  + gitee：https://gitee.com/newsun-boki/Ball3d
  + github:https://github.com/newsun-boki/3dBall
  + 博客： 