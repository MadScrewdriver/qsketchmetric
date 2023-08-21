Tutorial - Rendering your first parametric DXF file
========================================

**Let’s learn by example.**

In this tutorial you will render a parametric DXF file using the :class:`qsketchmetric.renderer.Renderer` module.

We’ll assume you have :ref:`QSketchMetric installed <installation-section>` already.

First download the `tutorial.dxf <https://raw.githubusercontent.com/MadScrewdriver/qsketchmetric/main/docs/_static/DXF/tutorial.dxf>`_
file from the `QSketchMetric repository <https://github.com/MadScrewdriver/qsketchmetric>`_. It is an example of a
parametric DXF file that we will use in a tutorial.

To do so, open it and click `Ctrl+S` to save it to your computer.
As a convention, we’ll assume you saved it in a file called ``tutorial.dxf``.

Now, create a new file called ``render.py`` and place it in the same directory as ``tutorial.dxf``.

Open ``render.py`` in your favorite text editor and import the :class:`qsketchmetric.renderer.Renderer` module
as well as the :meth:`ezdxf.new` method::

        from qsketchmetric.renderer import Renderer
        from ezdxf import new

The first one will be used to render the parametric DXF file, the second one to create output
:class:`ezdxf.document.Drawing`.

Create an output :class:`ezdxf.document.Drawing` object using :meth:`ezdxf.new module::

        dxf = new()

Before we will render ``tutorial.dxf`` let's check it out in the `QCAD Professional <https://qcad.org/en/download>`_
CAD software to see briefly what it looks like `(File -> Open)`. This is what you should see:

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial1.png
   :alt: tutorial.dxf opened in QCAD Professional

   tutorial.dxf opened in QCAD Professional

.. note::
    To see how to parametrize a drawing, see :ref:`parametrization-section`.

We can see it is a parametric drawing of a chalice. To render it needs variable ``h`` that stands for height of the
chalice. Let's set it to ``50``::

        variables = {'h': 50}

Now we are ready to roll. Let's render the parametric DXF file::

        renderer = Renderer('example.dxf', dxf, variables)
        renderer.render()

Finally, save the output drawing::

        dxf.saveas('rendered_tutorial.dxf')

The whole code should look like this::

        from qsketchmetric.renderer import Renderer
        from ezdxf import new

        dxf = new()
        variables = {'h': 50}
        renderer = Renderer('example.dxf', dxf, variables)
        renderer.render()
        dxf.saveas('rendered_tutorial.dxf')

Now run the code::

            python render.py

Finally open ``rendered_tutorial.dxf`` in ``QCAD Professional``. This is what you should see:

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial2.png
   :alt: rendered_tutorial.dxf opened in QCAD Professional

   rendered_tutorial.dxf opened in QCAD Professional

As you can see, the parametric DXF file was rendered successfully and the chalice height is ``50``.

**Congratulation you renderer your first parametric DXF file!**
