"""Python datastructures

  - Datastructures supporting a functional sytle of programming
    - which don't throw exceptions,
      - when used syntactically properly,
    - avoid mutation, or pushing mutation to innermost scopes,
    - employ annotations, see PEP-649,
      - needs annotations module from __future__ package,
      - useful for LSP and other external tooling, and
      - runtime applications (not too familiar with these).
  - In their semantics, consistently
    - uses None for "non-existent" values
    - and never stores the Python builtin None object the datastructures.
  - Modules can be imported individually,
    - see the testing module for examples. 
"""
__version__ = "0.5.2.1"

from .functional import *
from .dqueue import *
from .stack import *
