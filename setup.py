from setuptools import setup, find_packages

setup(
    name="simpledb",
    version="0.1",
    description="Simple pure-Python LSM key-value storage engine.",
    url="http://github.com/benshanahan1/simpledb",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "flake8",
            "black",
            "pytest",
            "pytest-pep8",
            "pytest-cov",
        ],
    },
)
