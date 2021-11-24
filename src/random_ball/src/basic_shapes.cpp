/*
 * @Author: your name
 * @Date: 2021-11-24 14:37:44
 * @LastEditTime: 2021-11-24 14:52:31
 * @LastEditors: newsun-HP-Pavilion-Gaming-Laptop-15-dk0xxx
 * @Description: In User Settings Edit
 * @FilePath: /rmtrain_ws/src/random_ball/src/basic_shapes.cpp
 */
#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
 
 int main( int argc, char** argv )
 {
   ros::init(argc, argv, "basic_shapes");
   ros::NodeHandle n;
   ros::Rate r(1);
   ros::Publisher marker_pub = n.advertise<visualization_msgs::Marker>("visualization_marker", 1);
 
   uint32_t shape = visualization_msgs::Marker::CUBE;
 
   while (ros::ok())
   {
     visualization_msgs::Marker marker;
     
     marker.header.frame_id = "odom";
     marker.header.stamp = ros::Time::now();
 
     marker.ns = "basic_shapes";
     marker.id = 0;
     
     marker.type = shape;
 
     marker.action = visualization_msgs::Marker::ADD;
 
     marker.pose.position.x = 1;
     marker.pose.position.y = 1;
     marker.pose.position.z = 1;
     marker.pose.orientation.x = 0.0;
     marker.pose.orientation.y = 0.0;
     marker.pose.orientation.z = 0.0;
     marker.pose.orientation.w = 1.0;
     
     marker.scale.x = 2.0;
     marker.scale.y = 2.0;
     marker.scale.z = 2.0;
     
     marker.color.r = 0.0f;
     marker.color.g = 1.0f;
     marker.color.b = 0.0f;
     marker.color.a = 0.1;
 
     marker.lifetime = ros::Duration();

     while (marker_pub.getNumSubscribers() < 1)
     {
       if (!ros::ok())
       {
         return 0;
       }
       ROS_WARN_ONCE("Please create a subscriber to the marker");
       sleep(1);
     }
     marker_pub.publish(marker);

    r.sleep();
  }
}