# Python grscheller.datastructures PyPI Package

Data structures geared to different algorithmic use cases. Supportive of
a functional style of programming, yet still endeavor to be Pythonic.

## Overview

The data structures in this package:

* Allow developers to focus on the algorithms the data structures were
  designed to support.
* Take care of all the "bit fiddling" needed to implement data structure
  behaviors, perform memory management, and deal with edge cases.
* Mutate data structure instances safely by manipulating encapsulated
  data in protected inner scopes.
* Iterate over inaccessible copies of internal state allowing the data
  structures to safely mutate while iterators leisurely iterate. 
* Safely share data between multiple data structure instances by making
  shared data immutable and inaccessible to client code.
* Don't force exception driven code paths upon client code.
* Code to the "happy" path & provide simple FP tools for "exceptional"
  events.

Sometimes the real power of a data structure comes not from what it
empowers you to do, but from what it prevents you from doing.

### Package overview grscheller.datastructures

* [Data structures][1]
* [Functional Subpackage][2]
* [Core Subpackage][3]

### Detailed API for grscheller.datastructures package

* [Detailed grscheller.datastructures API's][4]

### Design choices

#### None as "non-existence"

As a design choice, Python `None` is semantically used by this package
to indicate the absence of a value.

How does one store a "non-existent" value in a very real data structure?
Granted, implemented in CPython as a C language data structure, the
Python `None` "singleton" builtin "object" does have a sort of real
existence to it. Unless specifically documented otherwise, `None` values
are not stored to these data structures as data.

`Maybe` & `Either` objects are provided in the functional sub-package as
better ways to handle "missing" data.

#### Methods which mutate objects don't return anything.

For the main data structures at the top level of this package, methods
which mutate the data structures do not return any values. I try to
follow the Python convention followed by the builtin types of not
returning anything when mutated. Like the append method of the Python
list builtin.

#### Type annotations

This package was developed using Pyright to provide LSP
information to Neovim. This allowed the types to guide the design of
this package. 

Type annotations used in this package are extremely useful in helping
external tooling work well. These features are slated for Python 3.13
but work now in Python 3.11 by including *annotations* from
`__future__`.

The only good current information I have found on so far on type
annotations is in the Python documentation [here][5]. The PyPI pdoc3
package generates documentation based on annotations, docstrings, syntax
tree, and other special comment strings. See pdoc3 documentation
[here][6].

---

[1]: https://github.com/grscheller/datastructures/blob/main/README.d/Datastructures.md
[2]: https://github.com/grscheller/datastructures/blob/main/README.d/FunctionalSubpackage.md
[3]: https://github.com/grscheller/datastructures/blob/main/README.d/CoreSubpackage.md
[4]: https://grscheller.github.io/datastructures/
[5]: https://docs.python.org/3.13/library/typing.html
[6]: https://pdoc3.github.io/pdoc/doc/pdoc/#gsc.tab=0
