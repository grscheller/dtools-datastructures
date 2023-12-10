# grscheller.datastructures.core.carray modules

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
  * implemented with a Python List.

Mainly used as data storage for other data structures in the
grscheller.datastructures package. Freely stores None as a value.
