from setuptools import find_packages,setup

setup(
    name='agentic-trading-system',
    version='0.0.1',
    author='Anurag',
    packages=find_packages(),
    install_requires=['langchain','langgraph','lancedb','tavily-python','ploygon']
)