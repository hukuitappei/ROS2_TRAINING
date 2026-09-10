from glob import glob
from setuptools import find_packages, setup

package_name = "ros2_training_py"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="hukuitappei",
    maintainer_email="18567287+hukuitappei@users.noreply.github.com",
    description="Python subscriber examples for the ROS 2 training workspace.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={"console_scripts": ["py_listener = ros2_training_py.py_listener:main"]},
)
