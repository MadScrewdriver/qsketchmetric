
Semi-automatic parametrization
===============================
The :class:`qsketchmetric.semiautomatic.SemiAutomaticParameterization` module is used to semi-automatic parameterize
a DXF file. By semi-automatic, it means that the user has to manually customize the parameters of each entity after
the automatic parameterization process. Process includes:

    * Adding :ref:`MTEXT` entity.
    * Adding :ref:`VIRTUAL_LAYER` layer.
    * Adding default expression to each entity.
    * Joining entities with virtual lines in to the one coherent graph.

1. Make sure entities that are not :ref:`explicitly supported <explicit-section>` are packed in to an INSERT entity
   (block). If not, pack them using `QCAD Professional <https://qcad.org/en/download>`_ software. Otherwise, the
   entities will be deleted during the semi-automatic parametrization process.

2. If don't have already fire up a terminal and run python console::

        $ python

3. Define the path to the DXF file to parametrize::

        input_dxf_file = 'path/to/dxf/file.dxf'

4. **(Optional)** Define the path to the output parametrized DXF file.
    Default is `input_dxf_file` with `_param` appended to the file
    name contained in the `parametric` directory::

        output_dxf = 'path/to/output/parametrized_dxf/file.dxf'

5. **(Optional)** Define the expression that will be used to parametrize each entity. Default is `c` which
    stand for current length. See allowed expressions on the :ref:`manual parametrization page <parametrization-section>`.::

        expression = '?'

6. Parametrize the DXF file::

    from qsketchmetric.semiautomatic import SemiAutomaticParameterization
    sap = SemiAutomaticParameterization(input_dxf_file, default_value=expression, output_dxf_path=output_dxf)
    sap.parametrize()

7. Open the parametrized file in `QCAD Professional <https://qcad.org/en/download>`_, and customize the parameters.
Same as in the :ref:`manual parametrization <parametrization-section>` process.
