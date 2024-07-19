ARG WORKSPACE=/opt/ros/rtde_ws
FROM ros:humble
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ARG WORKSPACE

WORKDIR /opt/ros
RUN apt update && \
    apt install python3-pip -y && \
    pip install setuptools==58.2.0 && \
    pip install paho-mqtt && \
    git clone https://github.com/siderdax/ROS2_UR_RTDE_Receiver.git rtde_ws

WORKDIR $WORKSPACE/src
RUN git clone https://github.com/siderdax/ROS2_MQTT_PubSub.git ros_mqtt

WORKDIR $WORKSPACE
COPY ./src ./src
RUN source /ros_entrypoint.sh && colcon build --symlink-install

ENV WORKSPACE=$WORKSPACE
RUN sed --in-place --expression \
'$isource "$WORKSPACE/install/setup.bash"' \
/ros_entrypoint.sh

WORKDIR /
COPY ./configuration.xml .
ENV RTDE_HOST=localhost
ENV CONFIG_PATH=./configuration.xml
ENV FREQUENCY=10
ENV MQTT_HOST=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC="urRTDE"
CMD ["sh", "-c", "ros2 launch ur_rtde_receiver mqtt_publisher.launch.py \
rtde_host:=$RTDE_HOST \
rtde_config:=$CONFIG_PATH \
rtde_frequency:=$FREQUENCY \
mqtt_host:=$MQTT_HOST \
mqtt_port:=$MQTT_PORT \
topic_name:=$MQTT_TOPIC"]