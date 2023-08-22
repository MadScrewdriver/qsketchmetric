.. _MTEXT:

MTEXT
=====

Entity ``MTEXT`` is used to store the variables passed to the renderer and variables added during parametrization.
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
section. Those variables might come in handy during the parametrization process - to simplify the expressions describing
the entities. During parametrization variables can be used from the ``----- build in -----`` section
as well as from the ----- custom ----- section.


.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial11.png
   :alt: QCAD Professional with MTEXT dialog window opened

   QCAD Professional with MTEXT dialog window opened

.. warning::
    For the current version of QSketchMetric only **ONE** MTEXT entity is allowed in the DXF file

.. warning::
   MTEXT entity must be in a exact format as described above. Otherwise the parametrization process will fail.
