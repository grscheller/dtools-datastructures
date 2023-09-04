"""pytest testsuite

The testsuite can be either run against

1. The checked out main branch of https://github.com/grscheller/datastructures
   where we assume pytest has already been installed by either pip or some
   external package manager.

   $ export PYTHONPATH=/path/to/.../datastructures
   $ pytest --pyargs grscheller.datastructures

2. The pip installed package of a particular version from GitHub.

   $ pip install git+https://github.com/grscheller/datastructures@v0.2.1.0
   $ pytest --pyargs grscheller.datastructures

3. The pip installed package from PyPI (NOT YET PUSHED TO PyPI!!!)

   $ pip install grscheller.datastructures
   $ pytest --pyargs grscheller.datastructures

The pytest package was made a dependency of the grscheller.datastructures
package. This was to ensure the correct matching version of pytest was used to
run the tests. Otherwise, the wrong pytest executable running the wrong version
of Python might be found on your shell $PATH.
   
""" 
