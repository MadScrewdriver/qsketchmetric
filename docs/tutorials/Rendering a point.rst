Tutorial - Rendering a point
============================

**Let’s learn by example.**

In this tutorial, we will learn how to render a point using the :class:`qsketchmetric.renderer.Renderer` module.

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

Rendering a point is dead simple with QSketchMetric. All you need to do is to create a ``POINT``
entity on the :ref:`VIRTUAL_LAYER`. `(Draw -> Point -> Single Point)`
**The ``POINT`` must be connected to the other entities!**


Next you need to add a parameter to the point. To do so select the point and scroll down the
``Property Editor`` to the ``Custom`` section. Click on the red plus button and add the parameter.

    * ``Name`` should be: `name`.
    * ``Value`` should be: `variable_name` you desire.

`variable_name` will be returned by the renderer with new rendered coordination of the point.

Added point should look like this:

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial8.png
   :alt: Added point

   Added point

That is all! Now you can save the file and render it with :meth:`qsketchmetric.renderer.Renderer.render` method::

    from qsketchmetric.renderer import Renderer
    from ezdxf import new
    from ezdxf import units

    output_dxf = new()
    output_dxf.units = units.MM
    variables = {'h': 50}
    renderer = Renderer('tutorial.dxf', output_dxf, variables)
    variables = renderer.render()
    print(variables)

    output_dxf.saveas('rendered_tutorial.dxf')

``tutorial.dxf`` will be rendered on to the ``output_dxf`` :class:`ezdxf.document.Drawing` and rendered variable
from the :ref:`VIRTUAL_LAYER` will be contained in the ``variables`` dictionary with the following content::

    {
        "foot_point": (20, 10)
    }

**(20, 10)** is the rendered coordinate of the point.

**Congratulation you renderer your first point using :meth:`qsketchmetric.renderer.Renderer.render` method!**
