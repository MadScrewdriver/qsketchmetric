Getting started
===============

QSketchMetric is a tool designed to interpret parametric DXF files and render them. Parametrizing of a DXF file happens
through **QCAD Professional's** CAD software, which is a commercial software. The parametrized DXF file is then interpreted
by QSketchMetric and rendered according to the mathematical expressions.


Why QSketchMetric?
------------------
QSketchMetric was born out of a genuine need. There was an evident demand for a Python tool capable of generating
**DXF 2D** drawings based on parametric descriptions, rendering them according to provided variables.
This tool enables a seamless workflow during the production process, particularly beneficial for devices
like **plotters**.

Typical Use Cases
   Consider a box's cutting layout: with ``qsketchmetric``, it can be dynamically rendered to adapt
   based on its desired size.

What is DXF file?
-----------------
DXF (Drawing Interchange Format, or Drawing Exchange Format) is a CAD data file format developed by Autodesk for
enabling data interoperability between AutoCAD and other programs.

DXF file versions supported
----------------------------
QSketchMetric supports DXF files newer or equal to **R13** (Introduced in 1994).

How the documentation is organized?
-----------------------------------
Documentation follows `diataxis <https://diataxis.fr>`_ structure.
It is divided into the following parts:

* :ref:`Tutorials <tutorials>` take you by the hand through a series of steps to start using QSketchMetric.
  Start here if you’re new to QSketchMetric.

* :ref:`How-to guides <how-to-guides>` are recipes. They guide you through the steps involved in addressing key problems and use-cases.
  They are more advanced than tutorials and assume some knowledge of how QSketchMetric works.

* :ref:`Explanation <explanation>` guides discuss key topics and concepts of QSketchMetric.

* :ref:`Reference guides <reference>` contain technical reference for all aspects of QSketchMetric’s machinery.
  They describe how it works but assume that you have a basic understanding of key concepts.
