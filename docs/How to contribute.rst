How to contribute
=================

Thank you for investing your time in contributing to our project! Any contribution you make will
be reflected on `QSketchMetric docs <https://qsketchmetric.readthedocs.io/>`_ Hall of Fame ✨.
In this guide you will get an overview of the
contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.

.. _issues:

Issues / Feature requests
-------------------------

Create a new issue
~~~~~~~~~~~~~~~~~~
If you spot a problem with the package, you have a question or want to request a new feature,
it's a good idea to add it as an issue.
`Search if an issue already exists <https://github.com/MadScrewdriver/qsketchmetric/issues>`_.
If a related issue doesn't exist, you can open a new issue using a relevant issue form.

Solve an issue
~~~~~~~~~~~~~~
Scan through our `existing issues <https://github.com/MadScrewdriver/qsketchmetric/issues>`_ to find one that interests
you. You can narrow down the search using labels as filters. See
`labels <https://github.com/MadScrewdriver/qsketchmetric/labels>`_ for more information.
As a general rule, we don’t assign issues to anyone. If you find an issue to work on, you are welcome to open a
PR with a fix.

Make changes
------------

1. `Fork the repo <https://docs.github.com/en/get-started/quickstart/fork-a-repo#fork-an-example-repository>`_
   so that you can make your changes without affecting the original project until you're ready to merge them.
2. `Create a new virtual environment <https://virtualenv.pypa.io/en/latest/user_guide.html>`_ for the project and
   source it.
3. Install the project dependencies using::

    pip install -r requirements-dev.txt

4. Create a working branch and start with your changes!

Commit your update
------------------

Commit the changes once you are happy with them. Don't forget to self-review to speed up the review process.
Here are some tips for self-review:

* Confirm that you added tests for your code
* Confirm that you added documentation for your code
* Confirm that the changes meet the user experience and goals outlined in the issue description
* Review the changes for technical accuracy.
* Confirm that the changes are consistent with the project's style and standards adherence to the
  `mypy <https://mypy-lang.org/>`_ .
* If there are any failing checks in your PR, troubleshoot them until they're all passing.

Pull request
------------

When you're finished with the changes, create a pull request, also known as a PR.

* Don't forget to link PR to issue if you are solving one.
* We may ask for changes to be made before a PR can be merged.
  As you update your PR and apply changes, mark each conversation as resolved.
* If you run into any merge issues, checkout this `git tutorial <https://github.com/skills/resolve-merge-conflicts>`_
  to help you resolve merge conflicts and other issues.

Your PR is merged!
------------------

Congratulations! QSketchMetric develops thanks to people like you. Thank you for your contribution!
Once your PR is merged, your contributions will be publicly visible on the
`QSketchMetric docs <https://qsketchmetric.readthedocs.io/>`_ Hall of Fame ✨.

