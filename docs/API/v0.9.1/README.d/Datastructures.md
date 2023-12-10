# grscheller.datastructures package level modules

Modules providing the package's top level data structures.

## Non-typed data structures

* [flarray module](#flarray-module)
* [ftuple module](#ftuple-module)
* [queue module](#queue-module)
* [stack module](#stack-module)

### flarray module

Provides a fixed length array of elements of different types.

* Class **FLArray**
  * O(1) data access
  * once created, guaranteed not to change size
  * will store None as a value due to fix length guarentees

### ftuple module

Provides a functional tuple-like object.

* Class **FTuple**
  * immutable
  * O(1) data access
  * does not store None values

### queue module

Provides a single & double ended queues. The queues are implemented with
a circular arrays and will resize themselve as needed.

* Class **DQueue**
  * O(1) pushes & pops either end
  * O(1) peaks either end
  * O(1) length determination
  * O(n) copy
  * does not store None values

* Class **SQueue**
  * O(1) pushes & pops
  * O(1) peak last in or next out
  * O(1) length determination
  * O(n) copy
  * does not store None values

These queues are implemented with circular arrays and will resize
themseves as needed.

### stack module

Provides a LIFO singlelarly linked data structure designed to share
data between different Stack objects.

* Class **PStack**
  * PStack objects are stateful with a procudural interface
  * safely shares data with other PStack objects
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy
  * does not store None values

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
