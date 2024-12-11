cmake_minimum_required(VERSION 3.0.2)
project(dine_bot)

## 찾을 ROS 패키지 선언
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  tf
  amcl
  joint_state_publisher
  robot_state_publisher
  roslaunch
)

## catkin 패키지 설정
catkin_package(
  CATKIN_DEPENDS rospy std_msgs sensor_msgs geometry_msgs nav_msgs tf amcl joint_state_publisher robot_state_publisher
)

## ROS 파이썬 파일과 URDF 파일을 위한 경로 설정
install(DIRECTORY launch urdf map rviz param scripts
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
catkin_install_python(PROGRAMS scripts/myagv_camera_publisher.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
catkin_install_python(PROGRAMS scripts/optimized_camera_publisher.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
catkin_install_python(PROGRAMS scripts/arduino_controller.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
catkin_install_python(PROGRAMS scripts/line_trace.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)



