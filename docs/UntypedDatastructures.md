# grscheller.datastructes package level modules (untyped)

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
