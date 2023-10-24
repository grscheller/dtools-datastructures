# grscheller.datastructures.iterlib module

Module of functions used to manipulate Python iterators.

### Functions for interators

* Function **mapIter**(iter: iterator[Any], f: Callable[[Any], Any]) -> Iterator[Any]
  * Lazily map a function over an iterator stream

* Function **concatIters**(*iter: iterator[Any]) -> Iterator[Any]
  * Sequentually concatenate multiple iterators into one

* Function **mergeIters**(*iter: iterator[Any]) -> Iterator[Any]
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
* Many iterators are themselves iterable
  * many just return a "self" reference when iterator is requested
  * an iterator need not be iterable
  * an iterable can return something other than itself
    * like a copy of itself so the original can safely mutate
