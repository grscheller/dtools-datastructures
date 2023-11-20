# grscheller.datastructures package level modules

Modules providing the package's top level data structures. Date
structure classes whose names begin with an "F" have functional
interfaces and are are immutable (like Python Tuples).

## Non-typed data structures

* [squeue module](#squeue-module): provides SQueue class
* [dqueue module](#dqueue-module): provides DQueue class
* [pstack module](#pstack-module): provides PStack class
* [fstack module](#fstack-module): provides FStack class
* [ftuple module](#ftuple-module): provides FTuple class
* [fclarray module](#fclarray-module): provides FCLArray class

### squeue module

Provides a single ended queue. The queue is implemented with a circular
arrays and will resize themselve as needed.

* Class **SQueue**
  * O(1) pushes & pops
  * O(1) peak last in or next out
  * O(1) length determination
  * O(n) copy
  * does not store None values

### dqueue module

Provides a double ended queue. The queue is implemented with a circular
arrays and will resize themselve as needed.

* Class **DQueue**
  * O(1) pushes & pops either end
  * O(1) peaks either end
  * O(1) length determination
  * O(n) copy
  * does not store None values

### pstack module

Provides a LIFO singlelarly linked data structure designed to share
data between different PStack objects.

* Class **PStack**
  * PStack objects are stateful with a procudural interface
  * safely shares data with other PStack objects
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy
  * does not store None values

### fstack module

Provides a LIFO singlelarly linked data structure designed to share
data between different FStack objects.

* Class **FStack**
  * FStack objects are immutable with a functional interface
  * safely shares data with other FStack objects
  * O(1) head, tail, and cons methods
  * O(1) length determination
  * O(1) copy
  * does not store None values

Implemented as a singularly linked list of nodes. The nodes themselves
are private to the module and are designed to be shared among different
Stack instances.

Stack objects themselves are light weight and have only two attributes,
a count containing the number of elements on the stack, and a head
containing either None, for an empty stack, or a reference to the first
node of the stack.

### fclarray module

Provides a constant length mutable array of elements of different types.
Any methods which mutate this data structure are guaranteed not to
change its size. Otherwise, it has a functional interface.

* Class **FCLArray**
  * O(1) data access
  * immutable length
  * immutable default value used in lieu of storing None as a value

### ftuple module

Provides a functional tuple-like object.

* Class **FTuple**
  * immutable
  * O(1) data access
  * does not store None values
