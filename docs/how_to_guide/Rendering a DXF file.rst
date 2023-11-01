
Rendering a DXF file
====================

0. Consider validating the DXF file before rendering it. This can be done by using the `QSketchMetric Validator <https://qsketchmetricvalidator.eu.pythonanywhere.com/>`_.
   will render::

    from ezdxf import new
    output_dxf = new()

.. warning::
        Remember to make sure that the output and input DXF files are configured in the same units. If not, you can
        change the units of the output DXF file by::

            output_dxf.units = units.MM

        `ezdxf <https://ezdxf.readthedocs.io/en/stable/>`_ by default uses meters as the unit of measurement.

2. **(Optional)** Define the variables that are described in ``---- build in -----`` section of :ref:`MTEXT` entity::

        variables = {'variable_name': 100}

3. Define the path to the parametrized DXF file::

        path = 'how_to_guide.dxf'

4. **(Optional)** Define an offset for the rendered entities::

        offset = (50, 50)

5. Render the file::

        from ezdxf import new
        output_dxf = new()
        output_dxf.units = units.MM

        path = 'how_to_guide.dxf'

        # Optional
        variables = {'variable_name': 100}
        offset = (50, 50)

        renderer = Renderer(
                            path,
                            output_dxf,
                            variables=variables,
                            offset=offset
                            )
        rendered_points = renderer.render()


.. note::
    :meth:`qsketchmetric.renderer.Renderer.render` method renders parametric DXF on to the output_dxf and returns
    rendered points from :ref:`VIRTUAL_LAYER` as a Dictionary