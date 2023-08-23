# QSketchMetric

[![CI](https://github.com/MadScrewdriver/qsketchmetric/actions/workflows/tests.yml/badge.svg)](https://github.com/MadScrewdriver/qsketchmetric/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/qsketchmetric/badge/?version=latest)](https://qsketchmetric.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/MadScrewdriver/qsketchmetric/graph/badge.svg?token=OBMRQRRHUQ)](https://codecov.io/gh/MadScrewdriver/qsketchmetric)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/qsketchmetric.svg)](https://pypi.org/project/qsketchmetric/)
[![Python 3](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11-blue.svg)](https://www.python.org/downloads/release/python-3114/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

**QSketchMetric** is a Python 2D **parametric DXF** rendering engine. Parametrization is done using 
[**QCAD Professional software**](https://qcad.org/en/download)

## ⚡️ Quickstart

```python

from qsketchmetric.renderer import Renderer
from ezdxf import new

output_dxf = new()
input_parametric_dxf_path = 'parametric.dxf'

renderer = Renderer(input_parametric_dxf_path, output_dxf)
renderer.render()

output_dxf.saveas('rendered_parametric.dxf')
```

## 📷 Demo showcase

![Example GIF](docs/_static/Media/readme.gif)

## ⚙️ Installation

The most common case is the installation by [**pip package manager**](https://pip.pypa.io/en/stable/installation/):

```bash
  pip install qsketchmetric
```

## 🎯 Features

-  Parametric **DXF** rendering
-  Easy dxf files parametrization using [**QCAD Professional software**](https://qcad.org/en/download)
-  Support for `LINE`,`CIRCLE`,`ARC` and `POINT` entities
-  Open source and daily maintained

## 📚 Documentation
Documentation is available at [**QSketchMetric docs**](https://qsketchmetric.readthedocs.io/en/latest/)

## 📈 Roadmap
Support for more entities is planned in the future. If you have any suggestions, please create an issue.
If you want to contribute, see `How to contribute` section in the documentation. I am open to any suggestions
and waiting for your pull requests!

## ⚠️ License
QSketchMetric is licensed under the [**MIT**](https://opensource.org/licenses/MIT) license. 
When using the QSketchMetric in your open-source project I would be grateful for a reference to the repository.
