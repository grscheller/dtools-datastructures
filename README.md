# Python grscheller.datastructures PyPI Package

Data structures geared to different algorithmic use cases. Supportive of
a functional style of programming, yet still endeavor to be Pythonic.

## Overview

The data structures in this package:

* Allow developers to focus on the algorithms the data structures were
  designed to support.
* Take care of all the "bit fiddling" needed to implement desired
  behaviors.
* Mutate data structure instance safely by pushing contained data to a
  protected inner scope. 
* Share data between data structure instances safely by pushing mutation
  to an outer scope and making shared immutable internal state
  inaccessible to client code.
* Allow for "lazy" evaluation avoiding race conditions by having
  iterators process non-mutating copies of data structure internal
  state.
* Don't force the raising of gratuitous exceptions upon client code
  leveraging this package.
* Code to the "happy" path & provide simple FP tools for "exceptional"
  events.

Sometimes the real power of a data structure comes not from what it
enables you to do, but from what it prevents you from doing.

### Package overview grscheller.datastructures

* [Non-Typed Data structures][1]
* [Functional Subpackage][2]
* [Iterator Library][3]

### Detailed API for grscheller.datastructures package

* [Data Structure API's][4]

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
List builtin.

The practice in most Functional Programming (FP) languages is to return
a reference to the mutated data structure. This allows the chaining of
mutating methods, which I find convenient.

I need to decide on which convention to adopt before this package
becomes a Beta release.

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

[1]: https://github.com/grscheller/datastructures/blob/main/README.d/NonTypedDatastructures.md
[2]: https://github.com/grscheller/datastructures/blob/main/README.d/FunctionalSubpackage.md
[3]: https://github.com/grscheller/datastructures/blob/main/README.d/IteratorLibraryModule.md
[4]: https://grscheller.github.io/datastructures/documentation.html
[5]: https://docs.python.org/3.13/library/typing.html
[6]: https://pdoc3.github.io/pdoc/doc/pdoc/#gsc.tab=0
