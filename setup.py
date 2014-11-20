from setuptools import setup

setup(
    name='av2hdf5',
    version='1.0',
    description='Extract video frames into an HDF5 file',
    long_description=open('README.rst').read(),
    author='Rich Wareham',
    author_email='rich.av2hdf5@richwareham.com',
    url='https://github.com/rjw57/av2hdf5',
    packages=[
        'av2hdf5',
    ],
    package_dir={'av2hdf5': 'av2hdf5'},
    setup_requires=['pip'],
    install_requires=[
        'av',
        'docopt',
        'enum34',
        'numpy',
        'pillow',
        'tables',
    ],
    license="BSD",
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'av2hdf5 = av2hdf5:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
