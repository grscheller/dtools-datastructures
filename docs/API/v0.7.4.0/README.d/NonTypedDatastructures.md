# grscheller.datastructures package level modules (non-typed)

Non-typed means that the data structure can hold data of any type
except for perhaps `None`.

## Non-typed data structures

* Circular Array: [Carray](#carray-module)
* Double Ended Queue: [Dqueue](#dqueue-module)
* Fixed Length Array: [FLarray](#flarray-module)
* FIFO Queue: [Queue](#queue-module)
* LIFO Stack: [Stack](#stack-module)

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

Mainly used as data storage for other data structures in this package.
Implemented with a Python List.

### dqueue module

Provides a double ended queue. The queue is implemented with
a circular array and will resize itself as needed.

* Class **Dqueue**
  * O(1) pushes & pops either end
  * O(1) peaks either end
  * O(1) length determination
  * O(n) copy

### flArray module

Provides a fixed length array of elements of different types.

* Class **FLarray**
  * O(1) data access
  * once created, guaranteed not to change size
  * will store None as a value due to fix length guarentees

### queue module

Provides a FIFO queue data structure.

* Class **Queue**
  * O(1) push & pop
  * O(1) peaks for last in or next out
  * O(1) length determination
  * O(n) copy

The queue is implemented with a circular array and will resize itself
as needed.

### stack module

Provides a LIFO singlelarly linked data structure designed to share
data between different Stack objects.

* Class **Stack**
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy

Implemented as a singularly linked list of nodes. The nodes themselves
are private to the module and are designed to be shared among different
Stack instances.

Stack objects themselves are light weight and have only two attributes,
a count containing the number of elements on the stack, and a head
containing either None, for an empty stack, or a reference to the first
node of the stack.
