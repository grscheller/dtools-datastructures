## Python grscheller.datastructures package

Data structures supporting a functional style of programming and
avoiding the raising of unnecessary exceptions. 

Why not just use Python builtin data structures like lists and
dictionaries directly? The data structures in this package internalize
the "bit fiddling" allowing your code to follow the "happy path" and
letting you concentrate on the algorithms for which these data
structures were tailored to support. Sometimes the real power of a data
structure comes not from what it enables you to do, but from what it
does not allow you to do.

Unlike many of the data structures in the standard library, these data
structures avoid throwing uncaught exceptions. Uncaught exceptions
indicating possible coding errors like "SyntaxError", "AttributeError",
"TypeError" and sometimes "IndexError" are permitted. Also
"StopIteration" is frequently deferred to client code since it is so
deeply baked into the Python language. Monadic data structures like
Maybe and Either are provided to deal with the "unhappy path."
In Python, exceptions do have their place, but only for iterators and
"exceptional" events.

Mutation is either avoided or pushed to the innermost scopes. Functional
methods like map and flatMap return copies instead of mutating the
originals. Iterators usually iterate over copies of the iterables that
produced them.

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
  * O(1) length determination
  * O(n) copy

### grscheller.datastructes.flArray module

Implements a fixed length array of element of different types.

* Class **FLArray**
  * O(1) data access
* will store None as value

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
   In [1]: from grscheller.datastructures.core import *
   
   In [2]: for aa in concatIters(iter([1,2,3,4,5]), iter(['a','b','c'])):
      ...:     print(aa)
      ...:
   1
   2
   3
   4
   5
   a
   b
   c
   
   In [3]: for aa in mergeIters(iter([1,2,3,4,5]), iter(['a','b','c'])):
      ...:     print(aa)
      ...:
   1
   a
   2
   b
   3
   c

   In [4]: for aa in mapIter(iter([1,2,3,42]), lambda x: x*x):
      ...:     print(aa)
      ...:
   1
   4
   9
   1764
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

A Python iterator is a stateful objects with a __next__(self) method
which either returns the next value or raises the StopIteration exception.
The Python builtin next() function returns the next value from the
iterator object.

An object is iterable if it has an __iter__(self) method. This method
can either return an iterator or be a generator. the Python iter()
builtin function returns an iterator when called with an iterable
object. 

* Objects can be iterable without being iterators.
  * the iter() function produces an iterator for the iterable object
  * for-loop systax effectively call iter() behind the scenes 
* Many iterators are themseves iterable
  * many just return a "self" reference when iterator is requested
  * an iterator need not be iterable
  * an iterable can return something other than itself
    * like a copy of itself so the original can safely mutate
