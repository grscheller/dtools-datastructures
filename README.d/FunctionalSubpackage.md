# Subpackage grscheller.datastructures.functional

Monadic data structures supporting a functional style of programming.

### Module maybe

* Class **Maybe**
  * Represents a possible non-existent value
  * Implements the Option Monad
  * Functions like a Union type
    * Some(value)
    * Nothing

* Function **Some**(value)
  * creates a Maybe which contains a value
  * if value = None, then a Maybe Nothing object created

* Object **Nothing**
  * Maybe object representing the absence of a value
  * A Nothing is not a singleton
    * new instances can be created by Some() or Some(None)
    * in tests
      * use equality semantics
      * not identity semantics

### Module either

* Class **Either**
  * Represents a single value in one of two mutually exclusive contexts
  * Implements a Left biased Either Monad
  * Functions like a Union type
    * Left(value)
    * Right(value)

* Function **Left**(value, right=None)
  * Creates a left type of Either, unless value=None or is missing
    * Otherwise returns a right type Either with value right
  * Typically containing an intermediate value of an ongoing calculation

* Function **Right**(value=None)
  * Creates a right type of Either
  * Typically containing a str type for an error message

### Module util 

* Function **maybeToEither**(m: Maybe, right: Any=None) -> Either
  * Convert a Maybe to a left biased Either

* Function **eitherToMaybe**(e: Either) -> Maybe
  * Convert an Either to a Maybe
