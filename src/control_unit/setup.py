from setuptools import find_packages, setup

package_name = 'control_unit'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='allan',
    maintainer_email='allan.menchik@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "coach_node = control_unit.coach:main",
            "game_watcher_node = control_unit.game_watcher:main"
        ],
    },
)
