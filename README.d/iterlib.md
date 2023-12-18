# grscheller.datastructures.core.iterlib module

### core.iterlib library

Module of functions used to manipulate Python iterators.

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

   In [3]: for aa in exhaust(iter([1,2,3,4]), iter(['a','b'])):
      ...:     print(aa)
      ...:
   1
   a
   2
   b
   3
   4
```

#### Iterators vs Generators

The distinction between generators, iterators, and being iterable can
be confusing.

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
  * Once StopIteration is raised, the iterator will no longer yield
    any more values.

A generator is a type of iterator implemented via a function where at
least one return statement is replaced by a yield statement. Python also
has syntax to produce generators from "generator comprehensions" similar
to the syntax used for "list comprehensions."

__Note:__ Using either a generator or generator comprehension for
a class's `__iter__` method will not only provide both of the above
iterator protocol methods, but the iterators created by `for ... in`
syntax and the `map` builtin are inaccessible to the rest of the code.
The datastructures package defensively uses cached copies of data in
such generators so that the original objects can safely mutate while the
iterators created can leisurely yield the container's past state.

#### Iterable vs being an Iterator 

Don't confuse an object being iterable with being an iterator.

An object is iterable if it has an `__iter__(self)` method. This method
can either return an iterator or be a generator. The Python `iter()`
builtin function returns an iterator when called with an iterable
object. Most containers are iterable but not themselves iterators.

Python, at least by CPython, does not force an "iterator" to follow
iterator protocol. The Python `next()` builtin returns the next value
from an object which has a `__next__(self)` method.

It is best practice to make all your classes with `__next__(self)`
methods follow interator protocol. Standard library modules and many
PyPI packages make the assumptions that "iterators" follow interator
protocol. The PyPI grscheller.datastructure package makes this
assumption too.

[1]: https://docs.python.org/3/library/stdtypes.html#iterator-types
