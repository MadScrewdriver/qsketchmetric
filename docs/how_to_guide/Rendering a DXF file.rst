
Rendering a DXF file
====================

1. If don't have already, create a :class:`ezdxf.document.Drawing` object to which the renderer
   will render::

    from ezdxf import new
    dxf = new()

2. **(Optional)** Define the variables that are described in "---- build in -----" section of :ref:`MTEXT` entity::

        variables = {'variable_name': 100}

3. Define the path to the parametrized DXF file::

        path = 'how_to_guide.dxf'

4. **(Optional)** Define an offset for the rendered entities::

        offset = (50, 50)

5. Render the file::

        renderer = Renderer(
                            path,
                            dxf,
                            extra_variables=variables,
                            offset_drawing=offset
                            )
        rendered_points = renderer.render()


.. note::
    :meth:`qsketchmetric.renderer.Renderer.render` method returns rendered points as Dictionary