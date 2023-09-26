# Python grscheller.datastructures package

Data structures supporting a functional style of programming and
avoiding the throwing of exceptions. 

Why not just use Python builtin data structures like lists and
dictionaries directly? The data structures in this package internalize
the "bit fiddling" allowing your code to follow the "happy path" and
letting you to concentrate on the algorithms for which these data
structures are tailored.

Unlike the standard library, and other similar "functional" data
structures, these data structures do not throw exceptions, except for
ones like "SyntaxError", "AttributeError" or "TypeError".

Mutation is either avoided or pushed to the innermost scopes. Functional
methods like map and flatMap return copies instead of mutating the
originals.

The None singleton object, actually a python interpreter builtin,
is consistently used as a sentinel value to indicate the absence of
a value. This is done for the data structure implementations, as well as
for their semantics. These data structures consistently uses None for
"non-existent" values. None is never stored in the data structures
themselves. How do you store something that does not exist?

Type annotations are necessary to help external tooling work well.
See PEP-563 & PEP-649. These features are slated for Python 3.13
but work now in Python 3.11 by including the annotations module from
the `__future__` package.

## Package modules

### grscheller.datastructes.functional
Datastructures supporting a functional style of programming in Python.

* Class Maybe
  * Implements the Option Monad
  * Functionally a Union type
    * Some(value)
    * Nothing

### grscheller.datastructes.dqueue
Implements double ended queue. The queue is implemented with a circular
array and will resize itself as needed.

* Class Dqueue
  * O(1) pushes & pops either end
  * O(1) length determination
  * O(n) copy

### grscheller.datastructes.stack
A LIFO stack data structure implemented with singularly linked
nodes. The Stack objects themselves are light weight and have only two
attributes, a count containing the number of elements on the stack, and
a head containing either None, for an empty stack, or the first node of
the stack. The nodes themselves are an implementation detail and are
private to the module. The nodes, and the data they contain, are
designed to be shared between different Stack instances.
          
* Class Stack
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy

