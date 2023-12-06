# grscheller.datastructures package level modules

Modules providing the package's top level data structures.

## Non-typed data structures

* [squeue module](#fifoQueue-module): provides FIFOQueue class
* [squeue module](#lifoQueue-module): provides LIFOQueue class
* [dqueue module](#doubleQueue-module): provides DoubleQueue class
* [pstack module](#stack-module): provides Stack class
* [fstack module](#fstack-module): provides FStack class
* [clarray module](#clarray-module): provides CLArray class
* [ftuple module](#ftuple-module): provides FTuple class

### fifoQueue module

Provides a single ended FILO queue.

* Class **FIFOQueue**
  * O(1) pushes & pops
  * O(1) peak last in or next out
  * O(1) length determination
  * O(n) copy
  * does not store None values

### lifoQueue module

Provides a single ended LIFO queue.

* Class **LIFOQueue**
  * O(1) pushes & pops
  * O(1) peak last in/next out
  * O(1) length determination
  * O(n) copy
  * does not store None values

### doubleQueue module

Provides a double ended queue. The queue is implemented with a circular
arrays and will resize themselve as needed.

* Class **DoubleQueue**
  * O(1) pushes & pops either end
  * O(1) peaks either end
  * O(1) length determination
  * O(n) copy
  * does not store None values

### stack module

Provides a LIFO singlelarly linked data structure designed to share
data between different Stack objects.

* Class **Stack**
  * Stack objects are stateful with a procudural interface
  * safely shares data with other Stack objects
  * O(1) pushes & pops to top of stack
  * O(1) length determination
  * O(1) copy
  * does not store None values

Implemented as a singularly linked list of nodes. The nodes themselves
are inaccessible to client code and are designed to be shared among
different Stack instances.

Stack objects themselves are light weight and have only two attributes,
a count containing the number of elements on the stack, and a head
containing either None, for an empty stack, or a reference to the first
node of the stack.

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

Similar to Stack objects but immutable with a functional interface.

### clarray module

Provides a constant length mutable array of elements of different types.
Any methods which mutate this data structure are guaranteed not to
change its length. In the event of None values being added or mapped
into the array, a configurable default value can be used in its place.
A "backing queue" can be configured to swap values into and out of the
array. If a backing queue is provided and non-empty, it is used in lieu
of the default value for None.

* Class **CLArray**
  * O(1) data access
  * immutable length
  * default value used in lieu of storing None as a value
  * an optional backing queue can be provided

### ftuple module

Provides a functional tuple-like object.

* Class **FTuple**
  * immutable
  * O(1) data access
  * does not store None values
