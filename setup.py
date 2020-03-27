from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='badwing',
    packages=find_packages(),
    include_package_data=True,
    use_scm_version = {
        "local_scheme": "no-local-version"
    },
    setup_requires=['setuptools_scm'],

    install_requires=requirements,
    entry_points={"console_scripts": ["badwing = badwing.commands:cli"]},
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