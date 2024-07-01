# PyPI grscheller.datastructures Project

Python package of data structures which support the use and
implementation of algorithms.

* Functional & imperative programming styles supported
* FP supported but project endeavors to remain Pythonic
* Methods which mutate objects don't return anything
* [grscheller.datastructures][1] project on PyPI
* [Detailed API documentation][2] on GH-Pages
* [Source code][3] on GitHub

## Overview

Data structures allowing developers to focus on the algorithms they are
using instead of all the "bit fiddling" required to implement behaviors,
perform memory management, handle coding edge cases, and dealing with
exceptional events. These data structures allow iterators to leisurely
iterate over inaccessible copies of internal state while the data
structures themselves are free to safely mutate. They are designed to be
reasonably "atomic" without introducing inordinate complexity. Some of
these data structures allow data to be safely shared between multiple
data structure instances by making shared data immutable and
inaccessible to client code.

This package does not force functional programming paradigms on client
code, but provide functional tools to opt into. It also tries to avoid
forcing unnecessary exception driven code paths upon client code.

Originally, as a design choice, this package treated Python `None` to
semantically indicate the absence of a value. With the advent of the
typing package, it was decided to treat `None` as any other Python
datatype. Tooling such as mypy or pyright can be used at the expense of
more runtime safety with the benefit of more runtime efficiency.

Sometimes the real power of a data structure comes not from what it
empowers you to do, but from what it prevents you from doing to
yourself.

---

[1]: https://pypi.org/project/grscheller.datastructures/
[2]: https://grscheller.github.io/datastructures/API/development/html/grscheller/datastructures/index.html
[3]: https://github.com/grscheller/datastructures
