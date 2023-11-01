.. _validator-tutorial:

Tutorial - Validation your first DXF file
===================================================

**Let’s learn by example.**

In this tutorial, we will learn how to validate a parametrized DXF file.

We’ll assume you have :ref:`QSketchMetric installed <installation-section>` already as well as
`QCAD Professional <https://qcad.org/en/download>`_

First **(If you don't have already from other tutorials)** download the `tutorial.dxf
<https://raw.githubusercontent.com/MadScrewdriver/qsketchmetric/main/docs/_static/DXF/tutorial.dxf>`_
file from the `QSketchMetric repository <https://github.com/MadScrewdriver/qsketchmetric>`_. It is an example of a
DXF file that we will validate in this tutorial.

To do so, open it and click `Ctrl+S` to save it to your computer.
As a convention, we’ll assume you saved it in a file called ``tutorial.dxf``.

First, let’s open the file in QCAD Professional. `(File -> Open)`

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/tutorial1.png
   :alt: QCAD Professional with `tutorial.dxf` opened

    QCAD Professional with `tutorial.dxf opened

As you can see, it is a simple drawing of a chalice. It is parametrized depending on the chalice height.
Changing the chalice height ``h`` variable will render the drawing accordingly.

Let’s validate the drawing. To do so, open the
`QSketchMetric Validator <https://qsketchmetricvalidator.eu.pythonanywhere.com/>`_. and login using your **GitHub** account.
It is as simple as clicking the `Login with GitHub` button. The first time you login, you will be asked to authorize the application to access your GitHub account.

After logging in, you will see the following screen:

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/validator.png
   :alt: QSketchMetric Validator

    QSketchMetric Validator

Click the `choose a file` button and select the `tutorial.dxf` file you saved earlier.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/select.png
   :alt: QSketchMetric Validator with `tutorial.dxf` selected

    QSketchMetric Validator with `tutorial.dxf` selected

Next, click the `Validate` button. **And what this! An error!**

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/error.gif
   :alt: QSketchMetric Validator with error message

    QSketchMetric Validator with error message

The error is telling us that the `h` variable is not defined.
This is because the validator does not know what the `h` variable is while
calculating the ``chalice_foot_radius`` variable.

Download the debug report by clicking the `Debug report` button and open it in QCAD Professional.
We can see that every entity got greyed out accept of the MTEXT entity. It is because the MTEXT entity is the
place where the error occurred while calculating the ``chalice_foot_radius`` variable.
Also the error message is displayed in the right bottom corner of the drawing.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/debug.png
   :alt: QCAD Professional with `debug.dxf` opened

    QCAD Professional with `debug.dxf opened

Let’s fix the error! To do so, we need to define the `h` variable. click the `validate another file` button and
select the `tutorial.dxf` file again. This time, before clicking the `Validate` button, click the `set vars` button.
The modal window will appear.

Add new variable using the **+** symbol.
In the `name` field, type `h` and in the `value` field, type `50`.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/variables.png
   :alt: QSketchMetric Validator variables modal window

    QSketchMetric Validator variables modal window

Close the modal window and click the `Validate` button. **A success!**
Entities, Variables and Cohesion are all green and we are presented with a success message as well as a download button
for rendered DXF file.

.. figure:: https://qsketchmetric.readthedocs.io/en/latest/_static/Media/success.gif
   :alt: QSketchMetric Validator with success message

    QSketchMetric Validator with success message

**Congratulation you validated your first parametric DXF file!**
