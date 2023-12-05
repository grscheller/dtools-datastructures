# grscheller.datastructures.core.carray modules

### circular_array module

Provides a double sided circular array.

* Class **CircularArray**
  * double sides circular array
  * amortized O(1) pushing/popping either end
  * O(1) length determination
  * O(1) indexing for getting & setting array values
    * Raises `IndexError` exceptions
  * automatically resizes itself as needed
  * implemented with a Python List.
  * freely store `None` as a value

Mainly used for data storage in a "has-a" with other data structures in
the grscheller.datastructures package.
