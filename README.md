.. raw:: html

    <embed>
      <meta name="google-site-verification" content="7qV6cnAznhWKEKV-V5fzRie0cPSHuPHrp_49RfO9CpI" />
      <meta http-equiv="refresh" content="0; url=https://github.com/MadScrewdriver/qsketchmetric" />
    </embed>
    
![QSketchMetric logo](https://raw.githubusercontent.com/MadScrewdriver/qsketchmetric/main/docs/_static/Media/logo_QSM.svg)

[![CI](https://github.com/MadScrewdriver/qsketchmetric/actions/workflows/tests.yml/badge.svg)](https://github.com/MadScrewdriver/qsketchmetric/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/qsketchmetric/badge/?version=latest)](https://qsketchmetric.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/MadScrewdriver/qsketchmetric/graph/badge.svg?token=OBMRQRRHUQ)](https://codecov.io/gh/MadScrewdriver/qsketchmetric)
![PyPI - Downloads](https://img.shields.io/pypi/dm/qsketchmetric)
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
from ezdxf import units

output_dxf = new()
output_dxf.units = units.MM

input_parametric_dxf_path = 'tutorial.dxf'
input_variables = {"h": 50}

renderer = Renderer(input_parametric_dxf_path, output_dxf,
                    variables=input_variables)
renderer.render()

output_dxf.saveas('tutorial_rendered.dxf')
```

## 📷 Demo showcase

![Demo GIF](https://raw.githubusercontent.com/MadScrewdriver/qsketchmetric/main/docs/_static/Media/readme.gif)

## ⚙️ Installation

The most common case is the installation by [**pip package manager**](https://pip.pypa.io/en/stable/installation/):

```bash
  pip install qsketchmetric
```

## 🎯 Features

-  Parametric **DXF** rendering
-  Easy dxf files parametrization using [**QCAD Professional software**](https://qcad.org/en/download)
-  Explicit support for parametrization of `LINE`,`CIRCLE`,`ARC`, `POINT` entities
-  Support for parametrization of `LWPOLYLINE`, `POLYLINE`, `SPLINE`, `ELLIPSE`, `MTEXT`, `TEXT` **etc.** entities using `INSERT` entity.
-  Open source and daily maintained

## 📚 Documentation
Documentation is available at [**QSketchMetric docs**](https://qsketchmetric.readthedocs.io/en/latest/)

## 📈 Roadmap
Explicit support for more entities is planned in the future. If you have any suggestions, please create an issue.
If you want to contribute, see `How to contribute` section in the documentation. I am open to any suggestions
and waiting for your pull requests!

## ⚠️ License
QSketchMetric is licensed under the [**MIT**](https://opensource.org/licenses/MIT) license. 
When using the QSketchMetric in your open-source project I would be grateful for a reference to the repository.

## 🏆 Hall of fame
This project exists thanks to all the people who contribute. Thank you!

![GitHub Contributors Image](https://contrib.rocks/image?repo=MadScrewdriver/qsketchmetric)
