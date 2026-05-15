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
    node_camera_2_gz_bridge = Node(
        name='camera_2_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/etc/clearpath/sensors/config/camera_2.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    node_camera_2_static_tf = Node(
        name='camera_2_static_tf',
        executable='static_transform_publisher',
        package='tf2_ros',
        namespace='cpr_generic_e',
        output='screen',
        arguments=
            [
                '--frame-id'
                ,
                'camera_2_link'
                ,
                '--child-frame-id'
                ,
                'cpr_generic_e/robot/base_link/camera_2'
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

    node_camera_2_gz_image_bridge = Node(
        name='camera_2_gz_image_bridge',
        executable='image_bridge',
        package='ros_gz_image',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        arguments=
            [
                '/cpr_generic_e/sensors/camera_2/image'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/cpr_generic_e/sensors/camera_2/image'
                    ,
                    '/cpr_generic_e/sensors/camera_2/color/image'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_2/image/compressed'
                    ,
                    '/cpr_generic_e/sensors/camera_2/color/compressed'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_2/image/compressedDepth'
                    ,
                    '/cpr_generic_e/sensors/camera_2/color/compressedDepth'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_2/image/theora'
                    ,
                    '/cpr_generic_e/sensors/camera_2/color/theora'
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
    ld.add_action(node_camera_2_gz_bridge)
    ld.add_action(node_camera_2_static_tf)
    ld.add_action(node_camera_2_gz_image_bridge)
    return ld
