.. _VIRTUAL_LAYER:

VIRTUAL_LAYER
=============

VIRTUAL_LAYER will not be rendered in the final DXF file. It is used to store the virtual entities, which are needed
to parametrize the DXF file. Virtual layer will contain LINES and POINTS entities.

* POINTS entities will be rendered and returned as a ``dict`` by :meth:`qsketchmetric.renderer.Renderer.render` method
  in a form of::

    {
        "variable name": (x, y)
    }

  where ``x`` and ``y`` are the new coordinates of the renderer point.

* LINES entities will be used to join entities together. To form one coherent graph.
  They will be parametrized but not rendered. Used only to store the information about
  the relative position between entities.
