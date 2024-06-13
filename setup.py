from setuptools import setup, find_packages

setup(
    name="lazychange",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1",
        "gitpython>=3.1",
        "langchain>=0.2",
        "langchain-openai>=0.1",
        "langchain-community>=0.2",
    ],
    entry_points={
        "console_scripts": [
            "lazychange=lazychange.cli:cli",
        ],
    },
)
