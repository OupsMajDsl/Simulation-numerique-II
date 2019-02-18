from distutils.core import setup

setup(
    # Application name:
    name="GUI",

    # Version number (initial):
    version="1.0",

    # Application author details:
    author="Mathieu Maréchal",
    author_email="mathieu.marechal.etu@univ-lemans.fr",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "matplotlib",
        "numpy",
        "PyQt5",
        "sys"
    ],
)