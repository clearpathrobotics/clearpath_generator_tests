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
    node_camera_4_gz_bridge = Node(
        name='camera_4_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/etc/clearpath/sensors/config/camera_4.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    node_camera_4_static_tf = Node(
        name='camera_4_static_tf',
        executable='static_transform_publisher',
        package='tf2_ros',
        namespace='cpr_generic_e',
        output='screen',
        arguments=
            [
                '--frame-id'
                ,
                'camera_4_link'
                ,
                '--child-frame-id'
                ,
                'cpr_generic_e/robot/base_link/camera_4'
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

    node_camera_4_gz_image_bridge = Node(
        name='camera_4_gz_image_bridge',
        executable='image_bridge',
        package='ros_gz_image',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        arguments=
            [
                '/cpr_generic_e/sensors/camera_4/image'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/cpr_generic_e/sensors/camera_4/image'
                    ,
                    '/cpr_generic_e/sensors/camera_4/color/image'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_4/image/compressed'
                    ,
                    '/cpr_generic_e/sensors/camera_4/color/compressed'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_4/image/compressedDepth'
                    ,
                    '/cpr_generic_e/sensors/camera_4/color/compressedDepth'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_4/image/theora'
                    ,
                    '/cpr_generic_e/sensors/camera_4/color/theora'
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

    node_camera_4_gz_depth_bridge = Node(
        name='camera_4_gz_depth_bridge',
        executable='image_bridge',
        package='ros_gz_image',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        arguments=
            [
                '/cpr_generic_e/sensors/camera_4/depth_image'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/cpr_generic_e/sensors/camera_4/depth_image'
                    ,
                    '/cpr_generic_e/sensors/camera_4/depth/image'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_4/depth_image/compressed'
                    ,
                    '/cpr_generic_e/sensors/camera_4/depth/compressed'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_4/depth_image/compressedDepth'
                    ,
                    '/cpr_generic_e/sensors/camera_4/depth/compressedDepth'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_4/depth_image/theora'
                    ,
                    '/cpr_generic_e/sensors/camera_4/depth/theora'
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
    ld.add_action(node_camera_4_gz_bridge)
    ld.add_action(node_camera_4_static_tf)
    ld.add_action(node_camera_4_gz_image_bridge)
    ld.add_action(node_camera_4_gz_depth_bridge)
    return ld
