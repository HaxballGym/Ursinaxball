from setuptools import setup, find_packages
from setuptools.command.install import install

__version__ = None  # This will get replaced when reading version.py
exec(open("ursinaxball/version.py").read())

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="ursinaxball",
    packages=find_packages(),
    version=__version__,
    description="A recreation of the Haxball game using the ursina package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Wazarr",
    url="https://github.com/HaxballGym/ursinaxball",
    install_requires=[
        "numpy>=1.19",
        "msgpack>=1.0",
    ],
    license="Apache 2.0",
    license_file="LICENSE",
    keywords=["haxball", "ursina", "game"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
)
