from setuptools import setup, find_packages

VERSION = '1.6.3'
DESCRIPTION = 'Parametric 2D CAD'
LONG_DESCRIPTION = 'Parametric 2D drawings renderer using QCAD Professional'


setup(
    name="qsketchmetric",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Franciszek Łajszczak",
    author_email="franciszek@lajszczak.dev",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='CAD, QCAD, 2D, parametric, drawing, renderer, python renderer, python CAD, python 2d CAD, p'
             'python 2d drawing, python parametric drawing, python parametric CAD, python QCAD, QCAD python, '
             'parametric QCAD python, parametric QCAD, QCAD parametric, QCAD python parametric, QCAD python 2d,',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
