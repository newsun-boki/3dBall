<!--
 * @Author: your name
 * @Date: 2021-11-24 15:29:53
 * @LastEditTime: 2021-11-24 15:49:09
 * @LastEditors: newsun-HP-Pavilion-Gaming-Laptop-15-dk0xxx
 * @Description: In User Settings Edit
 * @FilePath: /rmtrain_ws/README.md
-->
# 3DBall

This is whole workspace of ros but not a single package.
## enviroments

+ opencv-python 3.4.4
  
+ numpy 1.20
  
+ ros melodic
# quick start


```bash
git clone https://github.com/newsun-boki/3dBall.git
catkin_make # rm -rf ./build ./devel if exits
source devel/setup.bash
```
```bash
roscore

rosrun random_ball simu.py

rosrun random_ball basic_shapes

rviz -d rmtrain_ws/src/random_ball/rm.rviz
```

![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211124/3dball.3jgtz0qnhjm0.gif)
