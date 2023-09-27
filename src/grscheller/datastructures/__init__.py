"""Python datastructures

  * Datastructures supporting a functional sytle of programming
    * which don't throw exceptions,
      * when used syntactically properly,
    * avoid mutation, or pushing mutation to innermost scopes,
    * employ annotations, see PEP-649,
      * needs annotations module from __future__ package,
      * useful for LSP and other external tooling, and
      * runtime applications (not too familiar with these).
  * In their semantics, consistently
    * uses None for "non-existent" values
  * Modules can be imported individually,
    * see the testing module for examples. 
  * semantic versioning
    * first digit signifies an event or epoch
    * second digit means breaking API changes (between PyPI releases)
    * third digit either means
      * API breaking changes (between GitHub commits)
      * API additions (between PyPI releases)
    * fourth digit either means
      * bugfixes or minor changes (between PyPI releases)
      * GitHub only thrashing and experimentation
"""
__version__ = "0.6.2.1"

from .functional import *
from .dqueue import *
from .stack import *
