.. _parametrization-section:

Manual parametrization
======================

Supported DXF Entities
----------------------
As of now, QSketchMetric supports the following DXF entities:
``LINE``, ``CIRCLE``, ``ARC``, ``POINT``

.. note::
    All calculations are done in **millimeters**.

What is needed?
-------------------
* `QCAD Professional <https://qcad.org/en/download>`_ is a commercial software, but it offers a free trial version. It
  is needed to embed the parameters into the DXF file. Community version of QCAD does not support this feature.
* A `DXF <https://pl.wikipedia.org/wiki/DXF>`_ file to parametrize.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial3.png
   :alt: QCAD Professional with DXF file to parametrize opened

   QCAD Professional with DXF file to parametrize opened

Manual parametrization
----------------------
1. Open the DXF file in QCAD Professional.  `(File -> Open)`
2. Add new layer called :ref:`VIRTUAL_LAYER` `(Layer -> Add Layer)`

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/layer.png
   :alt: QCAD Professional layer adding dialog window

   QCAD Professional layer adding window

3. Add :ref:`MTEXT` entity containing names of the variables passed to the renderer and variables added during
   parametrization. It can be placed anywhere. See :ref:`MTEXT` to get more information about the format of
   the entity. `(Draw -> Text)`


.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial11.png
   :alt: QCAD Professional with MTEXT dialog window opened

   QCAD Professional with MTEXT dialog window opened

4. Connect entities. Entities must be connected to each other.
      * **CIRCLES** - by their center point
      * **LINES** - by at lest one of their end points
      * **ARCS** - by their center point
      * **POINTS** - by their center point
   To achieve this add `LINE` entities `(Draw -> Line)` on to the :ref:`VIRTUAL_LAYER`. Those lines will connect
   the entities together and form one coherent graph. They won't be rendered in the final DXF file.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial5.png
   :alt: QCAD DXF drawing connected with lines

   DXF drawing connected with lines

5.
   Final step is to add parameters to the entities. To do so select the entity and scroll down the
   ``Property Editor`` to the ``Custom`` section. Click on the red plus button and add the parameter.

   * ``LINE``, ``CIRCLE`` and ``ARC``
      - ``Name`` must be: `c`.
      - ``Value`` contains the expression describing the entity. According to the table below.

      +--------------------+-----------------------------------------------------------------------------+
      |    Value           | Description                                                                 |
      +--------------------+-----------------------------------------------------------------------------+
      |      ``c``         | (constant) Entity length will not change                                    |
      +--------------------+-----------------------------------------------------------------------------+
      |      ``?``         | (undefined) Entity length will be calculated by the renderer.               |
      |                    | **Only if there is other path to the both end points of the line!**         |
      +--------------------+-----------------------------------------------------------------------------+
      |  ``v*10*sin(2)``   | (math expression) Entity length will be calculated from the math expression |
      |                    | (``v`` is a variable)                                                       |
      +--------------------+-----------------------------------------------------------------------------+

      Variables from the :ref:`MTEXT` entity can be used, as well as math expressions provided by
      `this list <https://github.com/AxiaCore/py-expression-eval/#available-operators-constants-and-functions>`_.

      There is an option to add **optional** ``line`` variable. This variables states the custom line style of the entity.
      ``Value`` should be in a format `<dash_width> <space_width>` seperated by a space. For example `1 2`.

   * ``POINT``
        - ``Name`` must be: `name`.
        - ``Value`` contains the name of the variable. This variable will be returned by
          the :meth:`qsketchmetric.renderer.Renderer.render` in a dictionary.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial12.png
   :alt: Entity with parameters

   Entity with parameters