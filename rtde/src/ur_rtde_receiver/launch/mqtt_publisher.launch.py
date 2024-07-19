from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    ExecuteProcess,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    rtde_host = LaunchConfiguration("rtde_host")
    rtde_config = LaunchConfiguration("rtde_config")
    rtde_frequency = LaunchConfiguration("rtde_frequency")
    mqtt_host = LaunchConfiguration("mqtt_host")
    mqtt_port = LaunchConfiguration("mqtt_port")
    mqtt_topic_name = LaunchConfiguration("topic_name")

    rtde_host_larg = DeclareLaunchArgument("rtde_host", default_value="192.168.56.101")
    rtde_config_larg = DeclareLaunchArgument(
        "rtde_config",
        default_value="install/ur_rtde_receiver/share/ur_rtde_receiver/config/configuration.xml",
    )
    rtde_frequency_larg = DeclareLaunchArgument("rtde_frequency", default_value="10")
    mqtt_host_larg = DeclareLaunchArgument("mqtt_host", default_value="localhost")
    mqtt_port_larg = DeclareLaunchArgument("mqtt_port", default_value="1883")
    mqtt_topic_name_larg = DeclareLaunchArgument("topic_name", default_value="urRTDE")

    rtde_node = Node(
        package="ur_rtde_receiver",
        remappings=[
            # ('/ur_rtde_data', topic_name),
        ],
        executable="receiver",
        parameters=[
            {
                "ur_rtde_env": {
                    "host": rtde_host,
                    "config": rtde_config,
                    "frequency": rtde_frequency,
                    "json": True,
                }
            },
        ],
    )

    mqtt_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [FindPackageShare("ros_mqtt"), "launch", "mqtt.launch.py"]
                )
            ],
        ),
        launch_arguments={
            "role": "publisher",
            "host": mqtt_host,
            "port": mqtt_port,
            "topic": mqtt_topic_name,
            "node_name": "ur_rtde_mqtt_pub",
            "topic_name": "ur_rtde_data",
        }.items(),
    )

    return LaunchDescription(
        [
            rtde_host_larg,
            rtde_config_larg,
            rtde_frequency_larg,
            mqtt_host_larg,
            mqtt_port_larg,
            mqtt_topic_name_larg,
            rtde_node,
            mqtt_launch,
        ]
    )
