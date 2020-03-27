import os

from setuptools import setup, find_packages

from badwing_setup.install import install
from badwing_setup.develop import develop

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

datadir = 'assets'
data_files = [(f'share/badwing/{d}', [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

setup(
    name='badwing',
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files,
    use_scm_version = {
        "local_scheme": "no-local-version",
        'write_to': 'badwing/version.py',
        'write_to_template': 'version = "{version}"',
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$'
    },
    setup_requires=['setuptools_scm'],
    cmdclass={
        'install': install,
        'develop': develop
    },
    install_requires=requirements,
    entry_points={"console_scripts": ["badwing = badwing.command:cli"]},
    author="Kurtis Fields",
    author_email="kurtisfields@gmail.com",
    description="Skateboarder/Platformer/Lepidopterist Game using Arcade & Pymunk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kfields/badwing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)