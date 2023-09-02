"""pytest testsuite

The testsuite can be either run against

1. The checked out main branch of https://github.com/grscheller/datastructures
   where we assume pytest has already been installed by either pip or some
   external package manager.

   $ export PYTHONPATH=/path/to/.../datastructures
   $ pytest --pyargs grscheller.datastructures

2. The pip installed package of a particular version from GitHub.

   $ pip install pytest
   $ pip install git+https://github.com/grscheller/datastructures@v0.2.0.2
   $ pytest --pyargs grscheller.datastructures

3. The pip installed package from PyPI (NOT YET PUSHED TO PYPI!!!)

   $ pip install pytest
   $ pip install grscheller.datastructures
   $ pytest --pyargs grscheller.datastructures

By default, virtual environments created by venv don't give access to the site
packages of the host Python used (at least this is the behavior for the
externally managed System Python on Arch Linux). Therefore, pytest should be
installed into whatever Python environment you are using. Otherwise, the wrong
pytest executable running the wrong version of Python could be found on your
shell $PATH.
   
""" 
