## Changelog: grscheller.datastrucures

### Version 0.3.1.0 - release date: 2023-09-09
* updated class Dqueue
  * added __eq__ method
  * added equality tests to tests/test_dqueue.py

### Version 0.3.0.2 - commit date: 2023-09-09

* created main_devel branch on GitHub
  * gives me a place to commit untested/broken code
  * allows for main branch to remain usable & unbroken
* improved docstrings

### Version 0.2.3.0 - commit date: 2023-09-06

* added __eq__ method to Stack class
* added some preliminary tests
  * more tests are needed
* worst case O(n)
  * will short circuit fast if possible

### Version 0.2.2.2 - release date: 2023-09-04

* decided base package should have no dependencies other than
  * Python version (>=2.10 due to use of Python match statement)
  * Python standard libraries
* made pytest an optional \[test\] dependency
* added src/ as a top level directory as per
  * https://packaging.python.org/en/latest/tutorials/packaging-projects/
  * could not do the same for tests/ if end users are to have access

### Version 0.2.1.0 - release date: 2023-09-03

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
* Python submodules:
  * dqueue - implements a double sided queue class Dqueue
  * stack - implements a LIFO stack class Stack
* Single maintainer project
  * semantic versioning
    * first digit signifies a major paradigm change or event
    * second digit means API breaking changes or minor paradigm change
    * third digit means API additions or substantial changes
    * fourth digit means bugfixes or minor changes
  * rolling release model
    * maintainer will not back port bugfixes to previous versions
    * main will be the only tracking branch on GitHub
    * github branches named "*_temp" are subject to deletion without notice 
