# grscheller.datastructures top level modules & data structures

Overview of package's top level modules and data structures.

## Top level modules

* [queue](#queue-module)
* [stack](#stack-module)
* [array](#array-module)
* [tup](#tup-module)

## Top level data structures

* [FIFO Queue](#class-fifoqueue): stateful FIFOQueue class
* [LIFO Queue](#class-lifoqueue): stateful LIFOQueue class
* [Double Ended Queue](#class-doublequeue): stateful DoubleQueue class
* [Stack](#class-stack): stateful (LIFO) Stack class
* [Functional Stack](#class-fstack): immutable (LIFO) FStack class
* [processing array](#class-parray): functional/stateful CLArray class
* [ftuple module](#class-ftuple): functional FTuple class

### queue module

Provides single ended FILO & LIFO queues. Also provides a double ended
queue data structure.

#### class FIFOQueue

Single ended First In, First Out (FIFO) stateful queue. The queue will
resize themselve as needed.

* O(1) pushes & pops
* O(1) peak last in or next out
* O(1) length determination
* O(n) copy
* does not store None values

#### class LIFOQueue

* O(1) pushes & pops
* O(1) peak last in/next out
* O(1) length determination
* O(n) copy
* does not store None values

#### class DoubleQueue

Double ended queue. The queue will resize themselve as needed.

* O(1) pushes & pops either end
* O(1) peaks either end
* O(1) length determination
* O(n) copy
* does not store None values

### stack module

Provides LIFO singlelarly linked data structures designed to share
data between different stack objects.

#### class Stack

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

#### class FStack

* FStack objects are immutable with a functional interface
* safely shares data with other FStack objects
* O(1) head, tail, and cons methods
* O(1) length determination
* O(1) copy
* does not store None values

Similar to Stack objects but immutable with a functional interface.

### array module

Provides a constant length mutable array of elements of different types.

#### class PArray

* O(1) data access
* size can be provided, otherwise sized to initial non-None data
* default value used in lieu of storing None as a value
* backing queue provided when more data is provided than PArray size
* default value used if not enough initial data provided
* optional backlog iterable can append more data to backing Queue

Provides a constant length mutable array of elements of different types.

Any methods which mutate this data structure are guaranteed not to
change its length. In the event of None values being added or mapped
into the array, a configurable default value can be used in its place.
A "backing queue" can be configured to swap values into and out of the
array. When non-empty, the backing queue is used in lieu of the default
value for None.

### tup module

Provides immutable tuple-like classes with functional interfaces.

#### class FTuple

Provides immutable tuple-like classes with a functional interfaces.

* immutable
* O(1) data access
* does not store None values

Planning to refactor for PyPI v0.11.1 or v0.12.0 release, depending on
the extend of API change.
