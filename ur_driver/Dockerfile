ARG WORKSPACE=/opt/ros/ur_ws
FROM ros:humble
WORKDIR $WORKSPACE

RUN apt update && \
    apt install ros-humble-ur -y

ENV ROBOT_MODEL=ur5e
ENV ROBOT_IP=192.168.56.101
CMD ["sh", "-c", "ros2 launch ur_robot_driver ur_control.launch.py ur_type:=$ROBOT_MODEL robot_ip:=$ROBOT_IP launch_rviz:=false"]