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
    node_ptu_0_gz_bridge = Node(
        name='ptu_0_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/etc/clearpath/sensors/config/ptu_0.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    node_ptu_0_gz_ptu_bridge = Node(
        name='ptu_0_gz_ptu_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        arguments=
            [
                '/ptu_0/cmd_pan@std_msgs/msg/Float64]gz.msgs.Double'
                ,
                '/ptu_0/cmd_tilt@std_msgs/msg/Float64]gz.msgs.Double'
                ,
                '/ptu_0/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/ptu_0/cmd_pan'
                    ,
                    '/cpr_generic_e/sensors/ptu_0/cmd_pan'
                )
                ,
                (
                    '/ptu_0/cmd_tilt'
                    ,
                    '/cpr_generic_e/sensors/ptu_0/cmd_tilt'
                )
                ,
                (
                    '/ptu_0/joint_states'
                    ,
                    '/cpr_generic_e/sensors/ptu_0/state'
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

    node_ptu_0_sim_relay = Node(
        name='ptu_0_sim_relay',
        executable='ptu_sim_relay_node',
        package='clearpath_generator_gz',
        namespace='cpr_generic_e/sensors/',
        output='screen',
        remappings=
            [
                (
                    'cmd'
                    ,
                    '/ptu/cmd'
                )
                ,
                (
                    'cmd_pan'
                    ,
                    '/cpr_generic_e/sensors/ptu_0/cmd_pan'
                )
                ,
                (
                    'cmd_tilt'
                    ,
                    '/cpr_generic_e/sensors/ptu_0/cmd_tilt'
                )
                ,
                (
                    'state'
                    ,
                    '/cpr_generic_e/sensors/ptu_0/state'
                )
                ,
                (
                    'joint_states'
                    ,
                    '/cpr_generic_e/platform/joint_states'
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
                    'pan_joint': 'ptu_0_pan'
                    ,
                }
                ,
                {
                    'tilt_joint': 'ptu_0_tilt'
                    ,
                }
                ,
            ]
        ,
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_arg_prefix)
    ld.add_action(node_ptu_0_gz_bridge)
    ld.add_action(node_ptu_0_gz_ptu_bridge)
    ld.add_action(node_ptu_0_sim_relay)
    return ld
