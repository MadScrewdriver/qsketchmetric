.. _debug:

Debug report
============

.. _error-messages:
Error messages
--------------
If error is related to specific entity, debug report contains detailed error message
with **handle** of problematic entity.

- **Variables validation error** - Error occurs in various situations when parsing variables. For example:
  wrong variable name, wrong variable type, undefined variable etc.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/verror.png
    :alt: Variables error

    Variables error

- **Entities validation error** - Error occurs when validating entities. For example: wrong entity type,
  wrong QCAD description, zero length line etc.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/eerror.png
   :alt: Entity error

   Entity error

- **Cohesion validation error** - Error occurs when validating cohesion. By cohesion we mean that all entities
  are connected to each other. Either directly or indirectly using :ref:`VIRTUAL_LAYER`.
  It is crucial that all entities form one connected graph to be able to find relative
  position of all entities. For example: line parametrized with '?' is not connected
  on both ends.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/cerror.png
   :alt: Cohesion error

   Cohesion error

- **Limit validation error** - Error occurs when user exceeds his limit of entities. For example:
  user has limit of 100 entities and his drawing has 150 entities. In this case see :ref:`Increase entities limit`.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/lerror.png
   :alt: Limit error

   Limit error


Dxf debug report
---------------
Debug raport itself is a DXF file. It contains all entities from input dxf file and additional information such as
error message in the bottom right corner of the report.


Every entity is grayed out accept problematic entity. Problematic entity is highlighted with signature color and is
placed on **DEBUG** layer.


In the case when more than one entity is problematic all those entities are placed on **DEBUG** layer and are
highlighted with signature color. For example: if there is cohesion error such as there are two separate graphs,
both graphs are highlighted with different color.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/cohesion.png
   :alt: QCAD Professional with `debug.dxf` opened. Cohesion error.

    QCAD Professional with `debug.dxf` opened. Cohesion error.
