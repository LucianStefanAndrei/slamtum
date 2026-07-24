from setuptools import find_packages, setup

package_name = 'slamtum_perception'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lucian',
    maintainer_email='stefan.andrei.lucian.design@gmail.com',
    description='Phase 4: semantic segmentation / detection on the image stream',
    license='MIT',
    entry_points={
        'console_scripts': [],
    },
)
