# Python grscheller.datastructures package

Unlike the standard library versions of some of these data structures,
these data structures do not throw exceptions. Why not just use Python
builtin data structures like lists and dictionaries directly? The data
structures in this package internalize the "bit fiddling" and allow you
to concentrate on the algorithms for which they are taylored.

The None "value" is consistently used as a sentinel value to indicate
the absence of a value. If None is pushed onto one of these data
structures, some additional care may be needed. If you do so, then the
len() function and isEmpty() methods are the best ways to determine when
the data structure no longer contains data. In this case, you can
repurpose None as your own sentinel value.

So that these data structures don't throw exceptions and can be reliably
used as iterators, some compromises were taken in regards to functional
purity.

## This package contains the follow modules

### dqueue
Implements double ended queue. The queue is implemented with a circular
array and will resize itself as needed.

* Class Dqueue
  * O(1) pushes & pops either end
  * O(1) length determination
  * O(n) copy

### stack
A LIFO stack data structure implemented with singularly linked
nodes. The Stack objects themselves are light weight and have only two
attributes, a count containing the number of elements on the stack, and
a head containing either None, for an empty stack, or the first node of
the stack. The nodes themselves are an implentation detail and are
private to the module. The nodes, and the data they contain, are
designed to be shared between different Stack instances.
          
* Class Stack
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy
