# Python grscheller.datastructures package

Data structures supporting a functional style of programming, avoiding
raising unnecessary exceptions, support either the sharing or the safe
encapsulation of data, yet still try to be Pythonic.

Why not just use Python builtin data structures like lists and
dictionaries directly? The data structures in this package allow you to

* focus on the algorithms these data structures were talored to support
* internalize the "bit fiddling" needed to implement the data structures
* code to the "happy path" and deal with errors without exceptions 
* safely handling mutation by
  * pushing it to protected innermost scopes
  * have iterators process non-mutating copies of internal state
* allow sharing of data by
  * pushing mutation to an outer scope
  * making immutable internal state inaccessible to client code

Sometimes the real power of a data structure comes not from what it
enables you to do, but from what it prvents you from doing.

As a design choice, None is semantically used by this package to
indicate the absence of a value. How does one store a "non-existent"
value in a very real datastructure? Implemented in CPython as
a C language data structure, the Python None "singleton" builtin
"object" does have a sort of real existence to it. Unless specifically
documented otherwise, None values are not stored in these data
structures.

Type annotations used in this package are extremely useful in helping
external tooling work well. See PEP-563 & PEP-649. These features are
slated for Python 3.13 but work now in Python 3.11 by including
*annotations* from `__future__`. This package was developed using
Pyright to provide LSP information to Neovim. This allowed the types
to guide the design of this package.

## grscheller.datastructes package level modules

### grscheller.datastructuses.circle module

Implements a double sided circular array with amortized O(1)
pushing/popping to/from either end, O(1) length determination,
and O(1) indexing for setting and getting values. Implemented
with a Python List. This datastructure automatically resizes
itself as needed.

Mainly used to help implement other data structures in this package,
this class is not opinionated regarding None as a value. It freely
stores and returns None values. Therfore, don't rely on using None as
a sentital value to determine if a circle circular array is empty or
not. Instead, if used in a boolean context, a circle returns false if
empty and true if not empty.

### grscheller.datastructes.dqueue module

Implements a double ended queue. The queue is implemented with
a circular array and will resize itself as needed. 

* Class **Dqueue**
  * O(1) pushes & pops either end
  * O(1) peaks either end
  * O(1) length determination
  * O(n) copy

### grscheller.datastructes.flArray module

Implements a fixed length array of elements of different types.

* Class **FLArray**
  * O(1) data access
* will store None as a value

### grscheller.datastructes.queue module

Implements a FIFO queue data structure. The queue is implemented with
a circular array and will resize itself as needed. 

* Class **Queue**
  * O(1) push & pop
  * O(1) peaks for last in or next out
  * O(1) length determination
  * O(n) copy

### grscheller.datastructes.stack module

Implements a LIFO stack data structure implemented with singularly
linked nodes. The Stack objects themselves are light weight and have
only two attributes, a count containing the number of elements on the
stack, and a head containing either None, for an empty stack, or the
first node of the stack. The nodes themselves are an implementation
detail and are private to the module. The nodes, and the data they
contain, are designed to be shared between different Stack instances.
          
* Class **Stack**
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy

## grscheller.datastructes.functional subpackage

FP Datastructures supporting a functional style of programming in Python.

### grscheller.datastructes.functional.maybe module

* Class **Maybe**
  * Represents a possible non-existent value
  * Implements the Option Monad
  * Functions like a Union type
    * Some(value)
    * Nothing

* Function **Some(value)**
  * creates a Maybe which contains a value
  * if value = None, then a Maybe Nothing object created

* Object **Nothing**
  * Maybe object representing the absence of a value
  * A Nothing is not a singleton
    * instances can be created by Some() or Some(None)
    * in tests
      * use equality semantics
      * not identity semantics

### grscheller.datastructes.functional.either module

* Class **Either**
  * Represents a single value in one of two mutually exclusive contexts
  * Implements a Left biased Either Monad
  * Functions like a Union type
    * Left(value)
    * Right(value)

* Function **Left(value, right=None)**
  * Creates a left type of Either, unless value=None or is missing
    * Otherwise returns a right type Either with value right
  * Typically containing an intermediate value of an ongoing calculation

* Function **Right(value=None)**
  * Creates a right type of Either
  * Typically containing a str type for an error message

### grscheller.datastructes.functional.util module

* Function **maybeToEither**

* Function **EitherToMaybe**

## grscheller.datastructes.iterlib module

Module of functions used in the manipulation of Python iterators.

### Functions for interators

* Function **mapIter**
  * Lazily map a function over an iterator stream

* Function **concatIters**
  * Sequentually concatenate multiple iterators into one

* Function **mergeIters**
  * Merge multiple iterator streams until one is exhausted

#### Examples

```python
   In [1]: from grscheller.datastructures.iterlib import *

   In [4]: for aa in mapIter(iter([1,2,3,42]), lambda x: x*x):
      ...:     print(aa)
      ...:
   1
   4
   9
   1764
   
   In [2]: for aa in concatIters(iter([1,2,3,4]), iter(['a','b'])):
      ...:     print(aa)
      ...:
   1
   2
   3
   4
   a
   b
   
   In [3]: for aa in mergeIters(iter([1,2,3,4]), iter(['a','b'])):
      ...:     print(aa)
      ...:
   1
   a
   2
   b
```

#### Why write my own iterator library module

Why not just use the itertools module? When I first created the iterlib
(formerly called core) module, I did not understand the distinction
between generators, iterators, and being iterable. They were all
conflated in my mind. Until I started coding with these concepts, the
itertools documentation just confused me even more.

#### Iterators vs generators

A generator is a type of iterator implemented via a function where at
least one return statement is replaced by a yield statement. Python also
has syntax to produce generators from "generator comprehensions" similar
to the syntax used to produce lists from "list comprehensions."

Don't confuse an object being iterable with being an iterator.

A Python iterator is a stateful objects with a \_\_next\_\_(self) method
which either returns the next value or raises the StopIteration exception.
The Python builtin next() function returns the next value from the
iterator object.

An object is iterable if it has an \_\_iter\_\_(self) method. This
method can either return an iterator or be a generator. the Python
iter() builtin function returns an iterator when called with an iterable
object. 

* Objects can be iterable without being iterators.
  * the iter() function produces an iterator for the iterable object
  * for-loop systax effectively call iter() behind the scenes 
* Many iterators are themseves iterable
  * many just return a "self" reference when iterator is requested
  * an iterator need not be iterable
  * an iterable can return something other than itself
    * like a copy of itself so the original can safely mutate
