from setuptools import setup, find_packages

setup(
    name="endutil",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
        "psutil",
        "distro",
        "py-cpuinfo"
    ],
    entry_points={
        'console_scripts': [
            'endutil = endutil.main:run',
        ],
    },
    package_data={
        "endutil": ["logos.txt"],
    },
    author="EndlessSb",
    description="A rich terminal system info tool like neofetch.",
)
