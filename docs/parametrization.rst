Parametrizing a DXF file
========================

Supported DXF Entities
----------------------
As of now, QSketchMetric supports the following DXF entities:
``LINE``, ``CIRCLE``, ``ARC``, ``POINT``

All calculations are done in **millimeters**.

What is needed?
-------------------
* `QCAD Professional <https://qcad.org/en/download>`_ is a commercial software, but it offers a free trial version. It
  is needed to embed the parameters into the DXF file. Community version of QCAD does not support this feature.
* A `DXF <https://pl.wikipedia.org/wiki/DXF>`_ file to parametrize.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/example1.png
   :alt: QCAD Professional with DXF file to parametrize opened

   QCAD Professional with DXF file to parametrize opened

Manual parametrization
----------------------
1. Open the DXF file in QCAD Professional.  `(File -> Open)`
2. Add new layer called `VIRTUAL_LAYER`_ `(Layer -> Add Layer)`

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/layer.png

3. Add `MTEXT`_ entity containing names of the variables passed to the renderer and variables added during
   parametrization. It can be placed anywhere. See `MTEXT`_ to get more information about the format of
   the entity. `(Draw -> Text)`

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/mtext.png

4. Connect entities. Entities must be connected to each other.
      * CIRCLES - by their center point
      * LINES - by at lest one of their end points
      * ARCS - by their center point
      * POINTS - by their center point
   To achieve this add a `LINE` entities `(Draw -> Line)` on to the `VIRTUAL_LAYER`_. Those lines will connect
   the entities together and form one coherent graph. They won't be rendered in the final DXF file.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/example2.png

5.
   Final step is to add parameters to the entities. To do so select the entity and scroll down the
   ``Property Editor`` to the ``Custom`` section. Click on the red plus button and add the parameter.

   * LINE, CIRCLE and ARC
      Parameter ``Name`` must be ``c``. In the ``Value`` field  add the expression describing the entity.
      Variables from the `MTEXT`_ entity can be used, as well as math expressions provided by
      `this list <https://github.com/AxiaCore/py-expression-eval/#available-operators-constants-and-functions>`_.
      Here is a list of valid ``Value`` expressions:

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

      There is an option to add **optional** ``line`` variable. This variables states the custom line style of the entity.
      ``Value`` should be in a format ``<dash_width> <space_width>`` seperated by a space. For example ``1 2``.

   * POINT
        Parameter ``Name`` must be ``name``. In the ``Value`` field should be the name of the variable.
        For example  ``happy_point``. This variable will be returned by the renderer as a ``dict``::

                {
                    "happy_point": (x, y)
                }

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/example3.png

6. Now check parametrized DXF file with ``Service coming soon`` to see if everything is correct and the file
   is ready to be rendered.


Semi-automatic parametrization
------------------------------
.. target-notes::
   This feature is still in development. It is not yet available.

.. _VIRTUAL_LAYER:

VIRTUAL_LAYER
-------------

VIRTUAL_LAYER will not be rendered in the final DXF file. It is used to store the virtual entities, which are needed
to parametrize the DXF file. Virtual layer will contain LINES and POINTS entities.

* POINT entities will be rendered and returned as a ``dict`` by :meth:`qsketchmetric.renderer.Renderer.render` method.
  There are many reasons why one would want new position of a point to be returned.
* LINE entities will be used to parametrize the DXF file. They will be used to join entities together. To form one
  coherent graph.

.. _MTEXT:

MTEXT
-----
This entity is used to store the variables passed to the renderer and variables added during parametrization.
The format of the text in the entity is as follows::

   Available variables:

   ----- build in -----
   c: const
   ?: undefined
   <variable_name>: <short_description>

   ----- custom -----
   <variable_name>: <variable_value>

Variables in the build in section are the variables that are passed to the renderer. They can be added
for better readability of parametrized DXF file. Custom variables can be also added to the custom
section. Those variables might come in handy during the parametrization process. To simplify the expressions describing
the entities. During parametrization variables can be used from the build in section and custom section.

.. warning::
    For current version of QSketchMetric only **ONE** MTEXT entity is allowed in the DXF file

.. warning::
   MTEXT entity must be in a exact format as described above. Otherwise the parametrization process will fail.
