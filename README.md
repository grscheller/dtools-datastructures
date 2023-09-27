# Python grscheller.datastructures package

Data structures supporting a functional style of programming and
avoiding the throwing of exceptions. 

Why not just use Python builtin data structures like lists and
dictionaries directly? The data structures in this package internalize
the "bit fiddling" allowing your code to follow the "happy path" and
letting you concentrate on the algorithms for which these data
structures were tailored to support.

Unlike the data structures in the standard library, these data
structures do not throw exceptions, except for ones like "SyntaxError",
"AttributeError" and "TypeError". This package supports the writing of
code that avoids the throwing of exceptions. Exceptions do have their
place, but only for "exceptional" events.

Mutation is either avoided or pushed to the innermost scopes. Functional
methods like map and flatMap return copies instead of mutating the
originals.

As a design choice, None is semantically used by this package to
indicate the absence of a value. How does one store a "non-existent"
value in a real datastructure? Implemented in CPython as
C language datastructures, the Python None "singleton" builtin object
does have a sort of real existence to it. Unless documented otherwise,
None is never "pushed" to any of these data structures. Dqueue is an
example of such an exception.

Type annotations are necessary to help external tooling work well. See
PEP-563 & PEP-649. These features are slated for Python 3.13 but work
now in Python 3.11 by including *annotations* from `__future__`.

## Package modules

### grscheller.datastructes.functional

FP Datastructures supporting a functional style of programming in Python.

* Class **Maybe**
  * Represents a possible non-existent value
  * Implements the Option Monad
  * Functionally a Union type
    * Some(value)
    * Nothing

* Class **Either**
  * Represents a single value in one of two mutually exclusive contexts
  * Implements a Left biased Either Monad
    * Left(value)
    * Right(value)

### grscheller.datastructes.dqueue

Double ended queue. The queue is implemented with a circular array and
will resize itself as needed. 

* Class **Dqueue**
  * O(1) pushes & pops either end
  * O(1) length determination
  * O(n) copy

If None values are pushed to this data structure, some care must be
taken when extracting them. Popping a None from a dqueue is
indestinguishable from popping from an empty dqueue. Empty Tuples ()
make for good sentinel values.

### grscheller.datastructes.stack

LIFO stack data structure implemented with singularly linked nodes. The
Stack objects themselves are light weight and have only two attributes,
a count containing the number of elements on the stack, and a head
containing either None, for an empty stack, or the first node of the
stack. The nodes themselves are an implementation detail and are private
to the module. The nodes, and the data they contain, are designed to be
shared between different Stack instances.
          
* Class Stack
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy
