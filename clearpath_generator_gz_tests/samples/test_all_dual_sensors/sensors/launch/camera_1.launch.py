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
    node_camera_1_gz_bridge = Node(
        name='camera_1_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/etc/clearpath/sensors/config/camera_1.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    node_camera_1_static_tf = Node(
        name='camera_1_static_tf',
        executable='static_transform_publisher',
        package='tf2_ros',
        namespace='cpr_generic_e',
        output='screen',
        arguments=
            [
                '--frame-id'
                ,
                'camera_1_link'
                ,
                '--child-frame-id'
                ,
                'cpr_generic_e/robot/base_link/camera_1'
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

    node_camera_1_gz_image_bridge = Node(
        name='camera_1_gz_image_bridge',
        executable='image_bridge',
        package='ros_gz_image',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        arguments=
            [
                '/cpr_generic_e/sensors/camera_1/image'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/cpr_generic_e/sensors/camera_1/image'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/image_raw'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_1/image/compressed'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/compressed'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_1/image/compressedDepth'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/compressedDepth'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_1/image/theora'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/theora'
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

    node_camera_1_gz_cmd_bridge = Node(
        name='camera_1_gz_cmd_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        arguments=
            [
                '/cpr_generic_e/sensors/camera_1/cmd_pan_vel@std_msgs/msg/Float64]gz.msgs.Double'
                ,
                '/cpr_generic_e/sensors/camera_1/cmd_tilt_vel@std_msgs/msg/Float64]gz.msgs.Double'
                ,
                '/cpr_generic_e/sensors/camera_1/pan_joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
                ,
                '/cpr_generic_e/sensors/camera_1/tilt_joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/cpr_generic_e/sensors/camera_1/pan_joint_state'
                    ,
                    '/cpr_generic_e/platform/joint_states'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_1/tilt_joint_state'
                    ,
                    '/cpr_generic_e/platform/joint_states'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_1/cmd_pan_vel'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/cmd_pan_vel'
                )
                ,
                (
                    '/cpr_generic_e/sensors/camera_1/cmd_tilt_vel'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/cmd_tilt_vel'
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

    node_ptz_action_server_node = Node(
        name='ptz_action_server_node',
        executable='ptz_controller_node',
        package='clearpath_generator_gz',
        namespace='/cpr_generic_e/sensors/camera_1',
        output='screen',
        remappings=
            [
                (
                    'image_in'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/image_raw'
                )
                ,
                (
                    'image_out'
                    ,
                    '/cpr_generic_e/sensors/camera_1/color/image'
                )
                ,
                (
                    'cmd/velocity'
                    ,
                    '/cpr_generic_e/sensors/camera_1/cmd/velocity'
                )
                ,
                (
                    'joint_states'
                    ,
                    '/cpr_generic_e/platform/joint_states'
                )
                ,
                (
                    'cmd_pan_vel'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/cmd_pan_vel'
                )
                ,
                (
                    'cmd_tilt_vel'
                    ,
                    '/cpr_generic_e/sensors/camera_1/_/cmd_tilt_vel'
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
                {
                    'camera_name': 'camera_1'
                    ,
                }
                ,
            ]
        ,
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_arg_prefix)
    ld.add_action(node_camera_1_gz_bridge)
    ld.add_action(node_camera_1_static_tf)
    ld.add_action(node_camera_1_gz_image_bridge)
    ld.add_action(node_camera_1_gz_cmd_bridge)
    ld.add_action(node_ptz_action_server_node)
    return ld
