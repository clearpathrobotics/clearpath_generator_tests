from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Include Packages
    pkg_clearpath_sensors = FindPackageShare('clearpath_sensors')

    # Declare launch files
    launch_file_flir_ptu = PathJoinSubstitution([
        pkg_clearpath_sensors, 'launch', 'flir_ptu.launch.py'])

    # Include launch files
    launch_flir_ptu = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_flir_ptu]),
        launch_arguments=
            [
                (
                    'parameters'
                    ,
                    '/etc/clearpath/sensors/config/ptu_0.yaml'
                )
                ,
                (
                    'namespace'
                    ,
                    'cpr_generic_e/sensors/ptu_0'
                )
                ,
                (
                    'robot_namespace'
                    ,
                    'cpr_generic_e'
                )
                ,
            ]
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_flir_ptu)
    return ld
