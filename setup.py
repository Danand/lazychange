from setuptools import setup, find_packages

setup(
    name="lazychange",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1",
        "openai>=1.31",
        "gitpython>=3.1",
    ],
    entry_points={
        "console_scripts": [
            "lazychange=lazychange.cli:cli",
        ],
    },
)
