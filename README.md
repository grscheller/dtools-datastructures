# PyPI grscheller.datastructures

Data structures geared to different algorithmic use cases. Supportive
of both functional and imperative programming styles while endeavoring
to remain Pythonic.

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
* Don't force functional programming paradigms on client code, but
  provide functional tools to opt into.
* Don't force exception driven code paths upon client code. Except for
  Python iterators and syntax errors, exceptions are for "exceptional"
  events.
* Purity is important, but not at the expense of practicality.
* Sometimes the real power of a data structure comes not from what
  it empowers you to do, but from what it prevents you from doing
  to yourself.
* [grscheller.datastructures API documentation][1]

### Design choices

#### None as "non-existence"

As a design choice, Python `None` is semantically used by this package
to indicate the absence of a value. It is used as an implementation
detail.

How does one store a "non-existent" value in a very real data structure?
Granted, implemented in CPython as a C language data structure, the
Python `None` "singleton" builtin "object" does have a sort of real
existence to it. Unless specifically documented otherwise, `None` values
are not stored to these data structures as data.

`Maybe` & `Either` objects are provided in the functional sub-package as
better ways to handle "missing" data. The emply tuple, `()` is a far
better sentital value since unlike `None` it is iterable.

#### Methods which mutate objects don't return anything.

Data structures when mutated do not return any values. This package
follows the convention used by Python builtins types of not returning
anything when mutated, like the append method of the Python list.

#### Type annotations

Type annotations are extremely helpul for external tooling to work well.
This package was developed using Pyright to provide LSP information to
Neovim. This allowed the types to guide the design of this package.
While slated for Python 3.13, type annotations work now for Python 3.11
by including *annotations* from `__future__`.

The best current information I have found so far on type annotations is
in the Python documentation [here][2]. The PyPI pdoc3 package generates
documentation based on annotations, docstrings, syntax tree, and other
special comment strings. See pdoc3 documentation [here][3].

#### Semantic Versioning

* Semantic versioning for PyPI releases:
  * first digit signifies a major event, epoch, or paradigm shift
  * second digit means
    * PyPI breaking API changes
    * PyPI major changes
  * third digit either means
    * PyPI API additions
    * PyPI bugfixes or minor changes
    * PyPI documentation updates
    * first development branch breaking API changes

---

[1]: https://grscheller.github.io/datastructures/
[2]: https://docs.python.org/3.13/library/typing.html
[3]: https://pdoc3.github.io/pdoc/doc/pdoc/#gsc.tab=0
