import os
from ament_index_python.packages import get_package_share_directory

import launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command

def generate_launch_description():

    package_name='rat20_movil' #<--- CHANGE ME

    # CONFIGURANDO EL WORLD: INICIO
      # Set the path to the world file
    world_file_name = 'terrainIndicador.world'
    # world_path = os.path.join(pkg_share, 'worlds', world_file_name)
    world_path = os.path.join(get_package_share_directory(package_name), 'worlds', world_file_name)

    world = LaunchConfiguration('world')

    declare_world_cmd = DeclareLaunchArgument(
    name='world',
    default_value=world_path,
    description='Full path to the world model file to load')

    # CONFIGURANCO EL WORLD: FIN

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )


    ejecutable = 'indicador_v1.py'
    ejecutable_path = os.path.join(get_package_share_directory(package_name), 'scripts', ejecutable)

    nodo_indicador= Node(
        package= None,
        executable= 'python3',
        # arguments=['/mnt/c/Ubuntu22o04PC/ros2-RAT20_movilIndicador/src/rat20_movil/scripts/indicador_v1.py'],
        arguments=[ejecutable_path],
        output= 'screen',
    )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file,'world': world}.items()
             )
    
    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'rat20_movil'],
                        output='screen')

    force_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["controladorTorque"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # Launch them all!
    return LaunchDescription([
        rsp,
        declare_world_cmd,
        gazebo,
        spawn_entity,
        force_drive_spawner,
        joint_broad_spawner,
        nodo_indicador
    ])
