from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Include Packages
    pkg_clearpath_common = FindPackageShare('clearpath_common')

    # Declare launch files
    launch_file_platform = PathJoinSubstitution([
        pkg_clearpath_common, 'launch', 'platform.launch.py'])

    # Include launch files
    launch_platform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_platform]),
        launch_arguments=
            [
                (
                    'robot_urdf'
                    ,
                    '/etc/clearpath/robot.urdf.xacro'
                )
                ,
                (
                    'config_control'
                    ,
                    '/etc/clearpath/platform/config/control.yaml'
                )
                ,
                (
                    'config_localization'
                    ,
                    '/etc/clearpath/platform/config/localization.yaml'
                )
                ,
                (
                    'config_twist_mux'
                    ,
                    '/etc/clearpath/platform/config/twist_mux.yaml'
                )
                ,
                (
                    'config_interactive_markers'
                    ,
                    '/etc/clearpath/platform/config/teleop_interactive_markers.yaml'
                )
                ,
                (
                    'config_teleop_joy'
                    ,
                    '/etc/clearpath/platform/config/teleop_joy.yaml'
                )
                ,
                (
                    'use_sim_time'
                    ,
                    'false'
                )
                ,
                (
                    'namespace'
                    ,
                    'cpr_generic_e'
                )
                ,
                (
                    'enable_ekf'
                    ,
                    'true'
                )
                ,
            ]
    )

    # Nodes
    node_micro_ros_agent = Node(
        name='micro_ros_agent',
        executable='micro_ros_agent',
        package='micro_ros_agent',
        namespace='cpr_generic_e',
        output='screen',
        arguments=
            [
                'udp4'
                ,
                '--port'
                ,
                '11411'
                ,
            ]
        ,
    )

    # Processes
    process_configure_mcu = ExecuteProcess(
        shell=True,
        cmd=
            [
                [
                    'export ROS_DOMAIN_ID=0;'
                    ,
                ]
                ,
                [
                    FindExecutable(name='ros2')
                    ,
                    ' service call platform/mcu/configure'
                    ,
                    ' clearpath_platform_msgs/srv/ConfigureMcu'
                    ,
                    ' "{domain_id: 0,'
                    ,
                    ' robot_namespace: \'cpr_generic_e\'}"'
                    ,
                ]
                ,
            ]
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_platform)
    ld.add_action(node_micro_ros_agent)
    ld.add_action(process_configure_mcu)
    return ld
