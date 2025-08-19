from setuptools import setup, find_packages

setup(
    name="stockhelper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.0",
        "pandas>=1.3.0",
        "plotly>=6.2.0"
    ],
    author="Zaid",
    description="A stock price library with local caching and interval-based data organization.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
