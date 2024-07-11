ARG WORKSPACE=/opt/ros/mqtt_ws
FROM ros:humble
ARG WORKSPACE

WORKDIR $WORKSPACE/src
RUN apt update && \
    apt install python3-pip -y && \
    pip install paho-mqtt && \
    git clone https://github.com/siderdax/ROS2_MQTT_PubSub.git

WORKDIR $WORKSPACE
RUN rosdep install -ry --from-paths src/ros_mqtt/ --ignore-src; \
    colcon build --symlink-install

ENV WORKSPACE $WORKSPACE
RUN sed --in-place --expression \
    '$isource "$WORKSPACE/install/setup.bash"' \
    /ros_entrypoint.sh

WORKDIR /
ENV MQTT_HOST=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=ros_mqtt_topic
ENV MQTT_ROLE=subscriber
ENV NODE_NAME=ros_mqtt
ENV ROS_TOPIC_NAME=mqtt_message
CMD ["sh", "-c", "echo Start $MQTT_ROLE $MQTT_HOST $MQTT_PORT $MQTT_TOPIC;ros2 launch ros_mqtt \
mqtt.launch.py \
role:=$MQTT_ROLE \
node_name:=$NODE_NAME \
host:=$MQTT_HOST \
port:=$MQTT_PORT \
topic:=$MQTT_TOPIC \
topic_name:=$ROS_TOPIC_NAME"]