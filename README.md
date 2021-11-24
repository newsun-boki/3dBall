<!--
 * @Author: your name
 * @Date: 2021-11-24 15:29:53
 * @LastEditTime: 2021-11-24 15:49:09
 * @LastEditors: newsun-HP-Pavilion-Gaming-Laptop-15-dk0xxx
 * @Description: In User Settings Edit
 * @FilePath: /rmtrain_ws/README.md
-->
# 视觉进阶培训1

三维弹球

## 依赖

+ opencv-python 3.4.4
  
+ numpy 1.20
  
+ ros melodic
# 快速开始


```bash
git clone https://github.com/newsun-boki/3dBall.git
cd 3dBall
catkin_make # rm -rf ./build ./devel if exits
source devel/setup.bash
```
```bash
roscore

rosrun random_ball simu.py #in 3dball directory

rosrun random_ball basic_shapes #in 3dball directory

rviz -d src/random_ball/rm.rviz #in 3dball directory
```


![](https://cdn.jsdelivr.net/gh/newsun-boki/img-folder@main/20211124/3dball.3jgtz0qnhjm0.gif)

( I add collide after the gif)
