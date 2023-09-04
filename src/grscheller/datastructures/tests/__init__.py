"""pytest testsuite

The testsuite can be either run against

1. The checked out main branch of https://github.com/grscheller/datastructures
   where we assume pytest has already been installed by either pip or some
   external package manager.

   $ export PYTHONPATH=/path/to/.../datastructures
   $ pytest --pyargs grscheller.datastructures

2. The pip installed package with test optional dependency from GitHub.

   $ pip install "grscheller.datastructures[test] @ git+https://git@github.com/grscheller/datastructures"
   $ pytest --pyargs grscheller.datastructures

3. The pip installed particular version of the package from GitHub.
   $ pip install pytest
   $ pip install git+https://github.com/grscheller/datastructures@v0.2.1.1
   $ pytest --pyargs grscheller.datastructures

4. The pip installed package from PyPI

   $ pip install grscheller.datastructures[test]
   $ pytest --pyargs grscheller.datastructures

The pytest package was made an project.optional-dependency of the datastructures
package. To ensure the correct matching version of pytest is used to run the
tests, pytest needs to be installed into the virtual environment, either
manually or via the [test] optional-dependency. Otherwise, the
wrong pytest executable running the wrong version of Python might be found on
your shell $PATH.
   
""" 
