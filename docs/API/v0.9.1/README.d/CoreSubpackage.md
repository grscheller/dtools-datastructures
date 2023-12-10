# grscheller.datastructures.core package

### carray module

Provides a double sided circular array.

* Class **Carray**
  * double sides circular array
  * amortized O(1) pushing/popping either end
  * O(1) length determination
  * automatically resizes itself as needed
  * will freely store `None` as a value
  * O(1) indexing for getting & setting array values
    * Raises `IndexError` exceptions
  * implemented with a Python List.

Mainly used as data storage for other data structures in the
grscheller.datastructures package. Freely stores None as a value.

### core.iterlib library

Module of functions used to manipulate Python iterators.

* Function **mapIter**(iter: iterator, f: Callable[[Any], Any]) -> Iterator
  * DEPRECATED - written before I knew Python map builtin
  * lazily map a function over an iterator stream

* Function **concat**(*iter: iterator) -> Iterator
  * DEPRECATED - use itertools.chain instead
  * Sequentually concatenate multiple iterators into one
  * pure Python version of itertools.chain

* Function **merge**(*iter: iterator) -> Iterator
  * Merge multiple iterator streams until one is exhausted

* Function **exhaust**(*iter: iterator) -> Iterator
  * Merge multiple iterator streams until all are exhausted

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

   In [2]: for aa in concat(iter([1,2,3,4]), iter(['a','b'])):
      ...:     print(aa)
      ...:
   1
   2
   3
   4
   a
   b

   In [3]: for aa in merge(iter([1,2,3,4]), iter(['a','b'])):
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

Python iterators are implemented, at least by CPython, as stateful
objects with a \_\_next\_\_(self) method which either returns the next
value or raises the StopIteration exception. The Python builtin next()
builtin function returns the next value from the iterator object.

An object is iterable if it has an \_\_iter\_\_(self) method. This
method can either return an iterator or be a generator. The Python
iter() builtin function returns an iterator when called with an iterable
object

* Objects can be iterable without being iterators.
  * the iter() function produces an iterator for the iterable object
  * for-loop systax effectively call iter() behind the scenes
* Many iterators are themselves iterable
  * many just return a "self" reference when iterator is requested
  * an iterator need not be iterable
  * an iterable can return something other than itself
    * like a copy of itself so the original is not depleted by the copy

But...

Officially, according to the [Python documentation][1], an iterator
object is required to support "iterator protocol" and must provide
the following two methods:

* iterator.__iter__()
  * Required to return the iterator object itself. This is required to
    allow both containers and iterators to be used with `for ... in`
    statements and with the map() built in function.
* iterator.__next__()
  * Return the next item from the iterator. If there are no further
    items, raise the StopIteration exception.

Note that by using a generator for a class's __iter__ method will not
only provide both of the the above methods, but the iteterators created
by `for ... in` syntax and the `map` builtin are inaccessible to the
rest of the code. This package defensively uses cache copies of data in
such generators so that the original objects can safely mutate while the
iterators created can leisurely yield the container's past state.

[1]: https://docs.python.org/3/library/stdtypes.html#iterator-types
