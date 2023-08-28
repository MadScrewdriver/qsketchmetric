Tutorial - Semi-automatic parametrization of a DXF file
=======================================================

**Let’s learn by example.**

In this tutorial, we will learn how to semi-automatic parametrize a DXF file.

We’ll assume you have :ref:`QSketchMetric installed <installation-section>` already as well as
`QCAD Professional <https://qcad.org/en/download>`_ and have already done the
:ref:`rendering tutorial <rendering-tutorial>` as well as :ref:`parametrization tutorial <parametrization-tutorial>`

First download the `tutorial_param.dxf
<https://raw.githubusercontent.com/MadScrewdriver/qsketchmetric/main/docs/_static/DXF/tutorial_param.dxf>`_
file from the `QSketchMetric repository <https://github.com/MadScrewdriver/qsketchmetric>`_. It is an example of a
DXF file that we will parametrize in this tutorial. It is a simple drawing of a chalice.
With every entity placed on the CUTTING layer.

To do so, open it and click `Ctrl+S` to save it to your computer.
As a convention, we’ll assume you saved it in a file called ``tutorial_param.dxf``.

Let’s start by firing up command line and starting the python interpreter::

    python

.. warning::
    Remember to activate your virtual environment if you are using one::

            source .venv/bin/activate


Next we need to import the :class:`qsketchmetric.semiautomatic.SemiAutomaticParameterization` module::

    from qsketchmetric.semiautomatic import SemiAutomaticParameterization

Now define the path to the input file we downloaded earlier::

    input_dxf_path  = "tutorial_param.dxf"

For the output file path and default parameter we will use default settings.

Now we are ready to roll. Let's parametrize the DXF file::

    sap = SemiAutomaticParameterization(input_dxf_path)
    sap.parameterize()

Parametrized file will be saved in the `parametric` directory, in the same directory as the input file.

Open the parametrized file in `QCAD Professional <https://qcad.org/en/download>`_,
and edit the parameters.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial13.png
   :alt: QCAD Professional with `parametric_tutorial_param.dxf` opened

    QCAD Professional with `parametric_tutorial_param.dxf` opened

Every entity parameter is now set to the default parameter. Let's change their  values.

To do so select the entities one by one and scroll down the
``Property Editor`` to the ``Custom`` section. Click on `c` parameter to edit it.

``Value`` contains the expression describing the entity. According to this table below:

  +--------------------+-----------------------------------------------------------------------------+
  |    Value           | Description                                                                 |
  +--------------------+-----------------------------------------------------------------------------+
  |      ``c``         | (constant) Entity length will not change                                    |
  +--------------------+-----------------------------------------------------------------------------+
  |      ``?``         | (undefined) Entity length will be calculated by the renderer.               |
  |                    | **Only if there is other path to the both end points of the line!**         |
  +--------------------+-----------------------------------------------------------------------------+
  |  ``c*2/5``         | (math expression) Entity length will be calculated from the math expression |
  |                    |                                                                             |
  +--------------------+-----------------------------------------------------------------------------+

You can change the value of the parameter to any of the above. For example, let's change the value of the
 chalice leg line to `2*c`. This will make the leg line 2 times longer.

That is it! You have successfully parametrized a DXF file. As you can see semi-automatic parametrization is
much faster and easier than manual parametrization.

**Congratulation!**
