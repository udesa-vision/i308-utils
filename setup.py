from setuptools import setup, find_packages

setup(
    name="i308-utils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "requests"
    ],
    author="Esteban Uriza",
    description="paquete de utilidades para tutoriales",
    url="https://github.com/udesa-vision/i308-utils",
)
