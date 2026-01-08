from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sentinelx",
    version="2.0.0",
    description="SentinelX - Red/Blue/Purple Team Security Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hackura",
    url="https://github.com/hackura/SentinelX",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "jinja2>=3.1.0",
        "weasyprint>=60.0",
        "svglib>=1.5.0",
        "reportlab>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sentinelX=sentinelx.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
