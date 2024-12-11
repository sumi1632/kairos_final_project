import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'dine_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'params'), glob('params/*')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
    ],
    install_requires=['setuptools', 'mysql-connector-python'],
    zip_safe=True,
    maintainer='soomi',
    maintainer_email='tnal1632@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
       	    'nav2_controller=dine_bot.nav2_controller:main',
       	    'db_manager_node=dine_bot.db_manager:main',
       	    'task_manager_node=dine_bot.task_manager:main',
       	    'mycobot_controller=dine_bot.mycobot_controller:main',
            'esp32_control_node = dine_bot.esp32_control_node:main',
            'suction_cup_node = dine_bot.suction_cup_node:main',
            'monitor_plc_node = dine_bot.monitor_plc_node:main',
        ],
    },
)
