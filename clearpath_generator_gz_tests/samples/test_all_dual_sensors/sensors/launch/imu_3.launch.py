from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    launch_arg_prefix = DeclareLaunchArgument(
        'prefix',
        default_value='',
        description='')

    prefix = LaunchConfiguration('prefix')

    # Nodes
    node_imu_3_gz_bridge = Node(
        name='imu_3_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/etc/clearpath/sensors/config/imu_3.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    node_imu_3_static_tf = Node(
        name='imu_3_static_tf',
        executable='static_transform_publisher',
        package='tf2_ros',
        namespace='cpr_generic_e',
        output='screen',
        arguments=
            [
                '--frame-id'
                ,
                'imu_3_link'
                ,
                '--child-frame-id'
                ,
                'cpr_generic_e/robot/base_link/imu_3'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/tf'
                    ,
                    'tf'
                )
                ,
                (
                    '/tf_static'
                    ,
                    'tf_static'
                )
                ,
            ]
        ,
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                }
                ,
            ]
        ,
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_arg_prefix)
    ld.add_action(node_imu_3_gz_bridge)
    ld.add_action(node_imu_3_static_tf)
    return ld
