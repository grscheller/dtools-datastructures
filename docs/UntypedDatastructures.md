## grscheller.datastructes package level modules (untyped)

### grscheller.datastructuses.carray module

Provides a double sided circular array.

* Class **Carray**
  * double sides circular array
  * amortized O(1) pushing/popping either end
  * O(1) length determination
  * automatically resizes itself as needed
  * will freely store `None` as a value
  * O(1) indexing for getting & setting array values
    * Raises `IndexError` exceptions

Mainly used as data storage for other data structures in this package.
Implemented with a Python List.

### grscheller.datastructes.dqueue module

Provides a double ended queue. The queue is implemented with
a circular array and will resize itself as needed.

* Class **Dqueue**
  * O(1) pushes & pops either end
  * O(1) peaks either end
  * O(1) length determination
  * O(n) copy

### grscheller.datastructes.flArray module

Provides a fixed length array of elements of different types.

* Class **FLarray**
  * O(1) data access
  * once created, guaranteed not to change size
  * will store None as a value due to fix length guarentees

### grscheller.datastructes.queue module

Provides a FIFO queue data structure.

* Class **Queue**
  * O(1) push & pop
  * O(1) peaks for last in or next out
  * O(1) length determination
  * O(n) copy

The queue is implemented with a circular array and will resize itself as
needed.

### grscheller.datastructes.stack module

Provides a LIFO singlelarly linked datastructure designed to share data
between different Stack objects.

* Class **Stack**
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy

Implemented as a singularly linked list of nodes. The nodes themselves
are private to the module and are designed to be shared amoung different
Stack instances.

Stack objects themselves are light weight and have only two attributes,
a count containing the number of elements on the stack, and a head
containing either None, for an empty stack, or a reference to the first
node of the stack.

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

* Function **eitherToMaybe**

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

Why not just use the Python itertools module? When I first created the
iterlib (formerly called core) module, the distinction between
generators, iterators, and being iterable were all conflated in my
mind. The itertools documentation didn't make sense to me until
I started implementing and using these types of tools.

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
method can either return an iterator or be a generator. The Python
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
