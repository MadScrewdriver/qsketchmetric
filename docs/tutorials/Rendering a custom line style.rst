Tutorial - Rendering a custom line style
========================================

**Let’s learn by example.**

In this tutorial, we will learn how to render a custom lines style using the :class:`qsketchmetric.renderer.Renderer` module.

We’ll assume you have :ref:`QSketchMetric installed <installation-section>` already as well as
`QCAD Professional <https://qcad.org/en/download>`_ and have already done the
:ref:`rendering tutorial <rendering-tutorial>` as well as :ref:`parametrization tutorial <parametrization-tutorial>`

First download the `tutorial.dxf <https://raw.githubusercontent.com/MadScrewdriver/qsketchmetric/main/docs/_static/DXF/tutorial.dxf>`_
file from the `QSketchMetric repository <https://github.com/MadScrewdriver/qsketchmetric>`_. It is an example of a
parametric DXF file that we will use in a tutorial.

To do so, open it and click ``Ctrl+S`` to save it to your computer.
As a convention, we’ll assume you saved it in a file called ``tutorial.dxf``.

Open ``tutorial.dxf`` in QCAD Professional, the result should look like this:

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial1.png
   :alt: tutorial.dxf opened in QCAD Professional

   tutorial.dxf opened in QCAD Professional

As you can see, it is a simple drawing of a chalice. With every entity placed on the CUTTING layer.


Rendering a custom line style is easy with QSketchMetric. All you need to do is to add a parameter to the entities.
Select the entitie where you want a custom line format and scroll down the ``Property Editor`` to the ``Custom``
section. Click on the red plus button and add the parameter.

    * ``Name`` should be: `line`.
    * ``Value`` should be a `ezdxf custom complex line pattern format <https://ezdxf.readthedocs.io/en/stable/tutorials/linetypes.html#removing-linetypes>`_.


In our example, we will use a a line pattern that looks like this: `--- BOWL ---- BOWL ---`. We will use it
for the bowl of the chalice. To do so, ``Value`` should be: `A,2,-1,["BOWL",STANDARD,S=.5,U=0.0,X=-0.1,Y=-.05],-2.5`.

    Where:
            * `A` - every line pattern starts with `A`
            * `2` - line length
            * `-1` - space length
            * `["BOWL",STANDARD,S=.5,U=0.0,X=-0.1,Y=-.05]` - `BOWL` part definition
            * `-2.5` - space length after the `BOWL` part

.. note::
        Remember to add a comma after every parameter and do not use whitespaces.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial9.png
   :alt: ``tutorial.dxf`` with added `line` parameters

   ``tutorial.dxf`` with added `line` parameters


That is all! Now you can save the file and render it with :meth:`qsketchmetric.renderer.Renderer.render` method::

    from qsketchmetric.renderer import Renderer
    from ezdxf import new
    from ezdxf import units

    output_dxf = new()
    variables = {'h': 50}
    output_dxf.units = units.MM
    renderer = Renderer('tutorial.dxf', output_dxf, variables)
    renderer.render()
    output_dxf.saveas('rendered_custom_line_tutorial.dxf')


.. note::
        Remember to make sure that the output and input DXF files are configured in the same units. That is why we
        set the units of the output DXF file to ``MM``.

Rendered file should look like this:

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial10.png
   :alt: rendered_custom_line_tutorial.dxf opened in QCAD Professional

   rendered_custom_line_tutorial.dxf opened in QCAD Professional

**Congratulation you renderer your first custom line!**
