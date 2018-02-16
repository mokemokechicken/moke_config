from setuptools import setup


requires = []


setup(
    name='moke_config',
    version='0.1',
    description='This is a config utility for tree structure, PyCharm complement and overriding by dictionary.',
    url='https://github.com/mokemokechicken/moke_config',
    author='mokemokechicken',
    author_email='mokemokechicken@gmail.com',
    license='MIT',
    keywords='config PyCharm utility',
    packages=[
        "moke_config",
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
)
