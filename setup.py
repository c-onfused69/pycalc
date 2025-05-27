from setuptools import setup, find_packages

setup(
    name="pycalc",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.__main__:main'
        ]
    },
    install_requires=[],
)