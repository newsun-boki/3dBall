# 前哨站中装甲板模拟系统

## Quik Start
```bash
git clone https://github.com/newsun-boki/3dBall.git
cd 3dBall
catkin_make # rm -rf ./build ./devel if exits
source devel/setup.bash #记得每打开一个终端都要source一下
```
```bash
#在Ball3D下
roscore

rosrun tower_simu simu.py 

rviz -d src/tower_simu/simu.rviz 
```

![](https://media.giphy.com/media/W29qk5CotLbdgLtycD/giphy-downsized-large.gif)