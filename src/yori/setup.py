import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'yori'

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
       	    'nav2_controller=yori.nav2_controller:main',
       	    'db_manager_node=yori.db_manager:main',
       	    'task_manager_node=yori.task_manager:main',
       	    'mycobot_controller=yori.mycobot_controller:main',
        ],
    },
)
