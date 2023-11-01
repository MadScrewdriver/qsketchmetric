.. _validator:


Validating a parametrized DXF file
===================================

QSketchMetric Validator
-----------------------
To verify the proper parametrization of a DXF file, use the
[**QSketchMetric Validator**](https://qsketchmetricvalidator.eu.pythonanywhere.com/). It is a web application that
allows to upload DXF file and check if it is properly parametrized. In the event of an error,
the app will provide full debug report. Including place where the error occurred in the DXF file and the error message.


Validation process
------------------

1. Go to [**QSketchMetric Validator**](https://qsketchmetricvalidator.eu.pythonanywhere.com/). For widgets and fields
   explanation (for example: tokens) see the `Widgets`_ section.

2. Upload a DXF file by clicking on the **Choose a file** button or drag and drop a file into the upload area.

3. Provide a variables needed for the parametrization. This are the variables on upon which the file is rendered.
   To do so utilize the **set vars** button and add as many variables as needed.

4. Click on the **Validate** button.

5.

    1. If the file is properly parametrized, the app will display a message **validating succeeded** and the rendered
       file will be available for download.

    2. If the file is not properly parametrized, the app will display an **error message** and a **debug report** will
       be available for download.

    3. If the DXF file contains more entities than your user account allows, the app will display an **error message**
       saying that the file contains more entities than the account allows.
       In this case, see the `Increase entities limit`_ section.


.. _Widgets:
Widgets
-------
- **Choose a file** - button that allows to choose a file from your computer.
- **Validate** - button that starts the validation process.
- **set vars** - button that allows to set variables needed for the parametrization.
- **entities** - field that displays the number of entities in a DXF file that can be validated with the account.
- **tokens** - field that displays the number of validations that can be performed with current entity limit. After
  each validation the number of tokens is decreased by one. When the number of tokens reaches zero, the user will revert
  to the default entity limit of 20 entities.
- **question mark** - button that displays a tooltip with a help center.
- **Increase entities limit** - button that tooltip  with a `Increase entities limit`_ section.

.. _Increase entities limit:
Increase entities limit
-----------------------
Should your project require a higher entity count, kindly reach out to
`franciszek@lajszczak.dev <mailto:franciszek@lajszczak.dev?subject=Increase%20entities%20limit&body=Username%3A%20%0ADesired%20entities%20limit%3A%20%0ANumber%20of%20tokens%3A%20>`_ .
Please provide your desired **entity limit**, your account **username**, and the number of validations **(tokens)**
needed.