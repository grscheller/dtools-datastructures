# Changelog: grscheller.datastrucures

## Overview

* Single maintainer project
  * semantic versioning
    * first digit signifies an event or epoch
    * second digit - API breaking changes or paradigm change
    * third digit - API additions or minor paradigm changes
    * fourth digit either means
      * bugfixes or minor changes (with PyPI releases)
      * github only thrashing and experimentation
  * rolling release model
    * maintainer will not back port bugfixes to previous versions
    * main branch will be the only tracking branch on GitHub
      * attempt to keep realatvely stable, but not fully tested
    * feature branch begin with "feature_" & are places to
      * explore new directions
      * commit potentially broken code
      * could be deleted from GitHub WITHOUT WARNING
    * PyPI releases are taged with a leading "v" on GitHub
      * semantic versioning more strict between PyPI releases
      * semantic versioning between GitHub commits a bit more subjective
        * only meaningfull GitHub commits will be listed below
        * all non-pulled PyPI releases will be tagged & listed below

## Versions

### Version 0.5.2.1 - PyPI release date: 2023-09-24
* data structures now support a much more FP style for Python 
  * implemented Maybe monad
  * introduces the use of type annotations for this effort
  * much better test coverage

### Version 0.5.0.0 - commit date: 2023-09-20
* begin work on a more functional approach
  * create a monadic Option class
  * Drop the subclassing of NONE
  * put this effort on a new branch: feature_maybe
* some flaws with previous approach
  * the OO redirection not best
    * for a class used in computationally intense contexts
    * adds way too much complexity to the design
  * some Python library probably already implemented this
    * without looking, these probably throw tons of exceptions
    * more fun implementing it myself
      * then being dissatified with someone else's design

### Version 0.4.0.0 - commit date: 2023-09-11
* subtle paradigm shift for Stack class
  * empty Stacks no longer returned for nonexistent stacks
    * like the tail of an empty stack
    * singleton Stack.stackNONE class object returned instead
  * Stack & _StackNONE classes inherit from _StackBase
  * still working out the API

### Version 0.3.0.2 - PyPI release date: 2023-09-09
* updated class Dqueue
  * added __eq__ method
  * added equality tests to tests/test_dqueue.py
* improved docstrings

### Version 0.2.3.0 - commit date: 2023-09-06

* added __eq__ method to Stack class
* added some preliminary tests
  * more tests are needed
* worst case O(n)
  * will short circuit fast if possible

### Version 0.2.2.2 - PyPI release date: 2023-09-04

* decided base package should have no dependencies other than
  * Python version (>=2.10 due to use of Python match statement)
  * Python standard libraries
* made pytest an optional \[test\] dependency
* added src/ as a top level directory as per
  * https://packaging.python.org/en/latest/tutorials/packaging-projects/
  * could not do the same for tests/ if end users are to have access

### Version 0.2.1.0 - PyPI release date: 2023-09-03

* first Version uploaded to PyPI
* https://pypi.org/project/grscheller.datastructures/
* Installable from PyPI
  * $ pip install grscheller.datastructures==0.2.1.0
  * $ pip install grscheller.datastructures # for top level version
* Installable from GitHub
  * $ pip install git+https://github.com/grscheller/datastructures@v0.2.1.0
* pytest made a dependency
  * useful & less confusing to developers and endusers
    * good for systems I have not tested on
    * prevents another pytest from being picked up from shell $PATH
      * using a different python version
      * giving "package not found" errors
    * for CI/CD pipelines requiring unit testing

### Version 0.2.0.2 - github only release date: 2023-08-29

* First version installable from GitHub with pip
* $ pip install git+https://github.com/grscheller/datastructures@v0.2.0.2

### Version 0.2.0.1 - commit date: 2023-08-29

* First failed attempt to make package installable from GitHub with pip

### Version 0.2.0.0 - commit date: 2023-08-29

* BREAKING API CHANGE!!!
* Stack push method now returns reference to self
* Dqueue pushL & pushR methods now return references to self
* These methods used to return the data being pushed
* Now able to "." chain push methods together
* Updated tests - before making API changes
* First version to be "released" on GitHub

### Version 0.1.1.0 - commit date: 2023-08-27

* grscheller.datastructures moved to its own GitHub repo
* https://github.com/grscheller/datastructures
  * GitHub and PyPI user names just a happy coincidence

### Version 0.1.0.0 - initial version: 2023-08-27

* Package implementing data structures which do not throw exceptions
* Did not push to PyPI until version 0.2
* Initial Python Datastructures for 0.1.0.0:
  * dqueue - implements a double sided queue class Dqueue
  * stack - implements a LIFO stack class Stack
