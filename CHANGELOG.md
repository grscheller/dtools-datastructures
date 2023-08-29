## Changelog: grscheller.datastrucures

### Version v1.0.0.0 - date: TBD

* First Version which will be uploaded to PyPI

### Version v0.2.0.0 - date: 2023-08-29

* BREAKING API CHANGE!!!
* Stack push method now returns reference to self
* Dqueue pushL & pushR methods now return references to self
* These methods used to return the data being pushed
* Now able to "." chain push methods together
* Updated tests - before making API changes
* First version to be "released" on GitHub

### Version v0.1.1.0 - date: 2023-08-27

* grscheller.datastructures moved to its own GitHub repo
* https://github.com/grscheller/datastructures
  * GitHub and PyPI user names just a happy coincidence

### Version v0.1.0.0 - date: 2023-08-27

* Package implementing data structures which do not throw exceptions
* Pre-release versions (0.X.Y.Z) won't be pushed to PyPI
* Python submodules:
  * dqueue - implements a double sided queue class Dqueue
  * stack - implements a LIFO stack class Stack
* Single maintainer project
  * semantic versioning
    * first digit signifies major feature additions
    * second digit signifies API breaking changes
    * third digit signifies API additions or substantial changes
    * fourth digit signifies signifies bugfixes or minor changes
      * uploaded to PyPI
      * tagged on GitHub
      * a "+" after version number signifies development only changes
  * rolling release model
    * maintainer will not back port bugfixes to previous versions
    * main will be the only tracking branch on GitHub
    * branches named "*_temp" are subject to deletion without notice 
