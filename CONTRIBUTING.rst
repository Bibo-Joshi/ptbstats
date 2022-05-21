How To Contribute
=================

Setting things up
-----------------

1. Fork the ``ptbstats`` repository to your github account.

2. Clone your forked repository of ``ptbstats`` to your computer:

   .. code-block:: bash

      $ git clone https://github.com/<your username>/ptbstats --recursive
      $ cd ptbstats

3. Add a track to the original repository:

   .. code-block:: bash

      $ git remote add upstream https://github.com/HirschHeissIch/ptbstats

4. Install dependencies:

   .. code-block:: bash

      $ pip install -r requirements.txt


5. Install pre-commit hooks:

   .. code-block:: bash

      $ pre-commit install

Finding something to do
#######################

If you already know what you'd like to work on, you can skip this section.

If you have an idea for something to do, first check if it's already been filed on the `issue tracker`_. If so, add a comment to the issue saying you'd like to work on it, and we'll help you get started! Otherwise, please file a new issue and assign yourself to it.

Instructions for making a code change
#####################################

The central development branch is ``master``, which should be clean and ready for release at any time. In general, all changes should be done as feature branches based off of ``master``.

Here's how to make a one-off code change.

1. **Choose a descriptive branch name.** It should be lowercase, hyphen-separated, and a noun describing the change (so, ``fuzzy-rules``, but not ``implement-fuzzy-rules``). Also, it shouldn't start with ``hotfix`` or ``release``.

2. **Create a new branch with this name, starting from** ``master``. In other words, run:

   .. code-block:: bash

      $ git fetch upstream
      $ git checkout master
      $ git merge upstream/master
      $ git checkout -b your-branch-name

3. **Make a commit to your feature branch**. Each commit should be self-contained and have a descriptive commit message that helps other developers understand why the changes were made.

   - You can refer to relevant issues in the commit message by writing, e.g., "#105".

   - Your code should adhere to the `PEP 8 Style Guide`_, with the exception that we have a maximum line length of 99.

   - Provide static typing with signature annotations. The documentation of `MyPy`_ will be a good start, the cheat sheet is `here`_.
   
   - Document your code. This project uses `sphinx`_ to generate static HTML docs. To build them, first make sure you have the required dependencies:

     .. code-block:: bash

        $ pip install -r docs/requirements-docs.txt

     then run the following from the PTB root directory:
   
     .. code-block:: bash
         
        $ make -C docs html

     or, if you don't have ``make`` available (e.g. on Windows):

     .. code-block:: bash

        $ sphinx-build docs/source docs/build/html

     Once the process terminates, you can view the built documentation by opening ``docs/build/html/index.html`` with a browser.

   - For consistency, please conform to `Google Python Style Guide`_ and `Google Python Style Docstrings`_. In addition, code should be formatted consistently with other code around it.

   - The following exceptions to the above (Google's) style guides applies:

        - Documenting types of global variables and complex types of class members can be done using the Sphinx docstring convention.

   - Please ensure that the code you write is well-tested.

   - Don’t break backward compatibility.

   - To actually make the commit (this will trigger tests for yapf, lint, pep8 and mypy automatically):

     .. code-block:: bash

        $ git add your-file-changed.py

   - Finally, push it to your github fork, run:

     .. code-block:: bash

      $ git push origin your-branch-name

4. **When your feature is ready to merge, create a pull request.**

   - Go to your fork on github, select your branch from the dropdown menu, and click "New merge request".

   - Add a descriptive comment explaining the purpose of the branch. This will tell the reviewer what the purpose of the branch is.

   - Click "Create merge request"

5. **Address review comments until all reviewers give LGTM ('looks good to me').**

   - When your reviewer has reviewed the code, you'll get an email. You'll need to respond in two ways:

       - Make a new commit addressing the comments you agree with, and push it to the same branch. Ideally, the commit message would explain what the commit does (e.g. "Fix lint error"), but if there are lots of disparate review comments, it's fine to refer to the original commit message and add something like "(address review comments)".

       - In addition, please reply to each comment. Each reply should be either "Done" or a response explaining why the corresponding suggestion wasn't implemented. All comments must be resolved before LGTM can be given.

   - Resolve any merge conflicts that arise. To resolve conflicts between 'your-branch-name' (in your fork) and 'master' (in the ``ptbstats`` repository), run:

     .. code-block:: bash

        $ git checkout your-branch-name
        $ git fetch upstream
        $ git merge upstream/master
        $ ...[fix the conflicts]...
        $ ...[make sure the tests pass before committing]...
        $ git commit -a
        $ git push origin your-branch-name

   - At the end, the reviewer will merge the pull request.

6. **Tidy up!** Delete the feature branch from both your local clone and the github repository:

   .. code-block:: bash

      $ git branch -D your-branch-name
      $ git push origin --delete your-branch-name

7. **Celebrate.** Congratulations, you have contributed to ``ptbstats``!

Style commandments
------------------

Specific commandments
#####################

- Avoid using "double quotes" where you can reasonably use 'single quotes'.

Assert comparison order
#######################

- assert statements should compare in **actual** == **expected** order.

For example (assuming ``test_call`` is the thing being tested):

.. code-block:: python

    # GOOD
    assert test_call() == 5

    # BAD
    assert 5 == test_call()

Properly calling callables
##########################

Methods, functions and classes can specify optional parameters (with default
values) using Python's keyword arg syntax. When providing a value to such a
callable we prefer that the call also uses keyword arg syntax. For example:

.. code-block:: python

   # GOOD
   f(0, optional=True)

   # BAD
   f(0, True)

This gives us the flexibility to re-order arguments and more importantly
to add new required arguments. It's also more explicit and easier to read.

Properly defining optional arguments
####################################

It's always good to not initialize optional arguments at class creation,
instead use ``**kwargs`` to get them. It's well known Telegram API can
change without notice, in that case if a new argument is added it won't
break the API classes. For example:

.. code-block:: python

    # GOOD
    def __init__(self, id, name, last_name=None, **kwargs):
       self.last_name = last_name

    # BAD
    def __init__(self, id, name, last_name=None):
       self.last_name = last_name


.. _`issue tracker`: https://github.com/HirschHeissIch/ptbstats/-/issues
.. _`developer' mailing list`: ptbstats@mahlerhome.de
.. _`PEP 8 Style Guide`: https://www.python.org/dev/peps/pep-0008/
.. _`sphinx`: http://sphinx-doc.org
.. _`Google Python Style Guide`: http://google.github.io/styleguide/pyguide.html
.. _`Google Python Style Docstrings`: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
.. _`MyPy`: https://mypy.readthedocs.io/en/stable/index.html
.. _`here`: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html