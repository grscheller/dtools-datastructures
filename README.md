# PyPI grscheller.datastructures Project

Python package of data structures which support the use and
implementation of algorithms.

* Functional & imperative programming styles supported
* FP supported but project endeavors to remain Pythonic
* Methods which mutate objects don't return anything
* [grscheller.circular-array][1] project on PyPI
* [Detailed API documentation][2] on GH-Pages
* [Source code][3] on GitHub

## Overview

The data structures in this package allow developers to focus on the
algorithms they are using instead of all the "bit fiddling" required to
implement behaviors, perform memory management, and handle edge cases
needed if Python builtin types were used instead. These data structures
allow iterators to leisurely iterate over inaccessible copies of
internal state while the data stuctures themselves safely mutate. Some
of these data structures allow data to be safely shared between multiple
data structure instances by making shared data immutable and
inaccessible to client code.

This package does not force functional programming paradigms on client
code, but provide functional tools to opt into. It also does not force
unnecessary exception driven code paths upon client code. Purity is
important, but not at the expense of practicality. Sometimes the real
power of a data structure comes not from what it empowers you to do, but
from what it prevents you from doing to yourself.

As a design choice, Python `None` is semantically used by this package
to indicate the absence of a value. While still freely used as an
implementation detail, `None` values are not stored in these data
structures. Functional `Maybe` and `Either` classes are provided in the
core.fp sub-module as better ways to handle "missing" data.

---

[1]: https://pypi.org/project/grscheller.datastructures/
[2]: https://grscheller.github.io/datastructures/API/development/html/grscheller/datastructures/index.html
[3]: https://github.com/grscheller/datastructures
