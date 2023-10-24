# Python grscheller.datastructures package

Data structures supporting a functional style of programming, yet still
endeavor to be Pythonic.

## Overview

The data structures in this package:

* Allow developers to focus on the algorithms the data structures were
  designed to support.
* Take care of all the "bit fiddling" needed to implement desired
  behaviors.
* Don't force the raising of gratuitous exceptions upon client code
  leveraging this package.
* Safely handle mutating contained data by pushing it to a protected
  inner scope. 
* Safely share data between data structure instances by pushing mutation
  to an outer scope and making shared immutable internal state
  inaccessible to client code.
* Allow for "lazy" evaluation avoiding race conditions by having
  iterators process non-mutating copies of data structure internal
  state.
* Code to the "happy" path & provide FP tools for "exceptional" events.

Sometimes the real power of a data structure comes not from what it
enables you to do, but from what it prevents you from doing.

### Data structure summary

* [Non-Typed Datastructures](docs/NonTypedDatastructures.md)
* [Functional Subpackage](docs/FunctionalSubpackage.md)
* [Iterator Library](docs/IteratorLibraryModule.md)

### Design choices

#### Type annotations

Type annotations used in this package are extremely useful in helping
external tooling work well. See PEP-563 & PEP-649. These features are
slated for Python 3.13 but work now in Python 3.11 by including
*annotations* from `__future__`. This package was developed using
Pyright to provide LSP information to Neovim. This allowed the types
to guide the design of this package.

#### None as "non-existence"

As a design choice, Python `None` is semantically used by this package
to indicate the absence of a value. How does one store a "non-existent"
value in a very real data structure? Granted, implemented in CPython as
a C language data structure, the Python `None` "singleton" builtin
"object" does have a sort of real existence to it. Unless specifically
documented otherwise, `None` values are not stored to these data
structures as data. `Maybe` & `Either` objects are provided as better
ways to handle "missing" data.

#### Methods which mutate objects don't return anything.

For methods which mutate their data structures, I try to follow the
Python convention of not returning anything, like the append method of
the Python List builtin object. Most functional programming languages
will return a reference to the data structure.
