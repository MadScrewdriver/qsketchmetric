from pkg_resources import parse_requirements
from setuptools import setup, find_packages  # type: ignore
from qsketchmetric import __version__

VERSION = __version__
DESCRIPTION = 'Python 2D parametric DXF rendering engine.'
LONG_DESCRIPTION = 'Python 2D parametric DXF rendering engine.'


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="qsketchmetric",
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme(),
    url="https://github.com/MadScrewdriver/qsketchmetric",
    project_urls={
        "Documentation": "https://qsketchmetric.readthedocs.io/",
    },
    author="Franciszek Łajszczak",
    author_email="franciszek@lajszczak.dev",
    license='MIT',
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    keywords='CAD, QCAD, 2D, parametric, drawing, renderer, python renderer, python CAD, python 2d CAD, p'
             'python 2d drawing, python parametric drawing, python parametric CAD, python QCAD, QCAD python, '
             'parametric QCAD python, parametric QCAD, QCAD parametric, QCAD python parametric, QCAD python 2d,',
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
    ]
)
