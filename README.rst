Justbases
=========

Purpose
-------
Conversion of a rational number to a representation in any base. Any
rational number can be represented as a repeating sequence in any base.
Any integer is representable as a terminating sequence in any base.

Motivation
----------
This facility does not seem to exist in standard Python numerical packages
or standard Python symbolic computation packages. Most likely that is
because it falls between the two, as it is precise numerical computation,
but involves a symbolic component, the possibly repeating sequence of
digits.

Algorithmic Complexity
----------------------
The complexity of operations that perform division in an arbitrary base
can be quite high. Most methods are annotated with an estimate of their
expected complexity in terms of the number of Python operations that they
make use of. No differentiation is made among different Python operations.
With respect to division in an arbitrary base, the complexity is bounded
by the value of the divisor, unless a precision limit is set.

Related Packages
----------------

* allyourbase: https://pypi.python.org/pypi/allyourbase

  Converts a variety of numeric types to str in arbitrary bases.
  Does not require one character to digit encoding, uses a digit separator.
  Requires rounding, does not do precise conversion, but does do
  conversion to any specified precision.

* python-baseconv: https://pypi.python.org/pypi/allyourbase

  Converts an int to a string using a one character to digit encoding.
  Also converts in the opposite direction.
  Does not handle arbitrary rationals and does not really handle conversion to
  large bases, e.g., 1024, as such conversion would require 1024 distinct
  characters.

* python-radix: https://pypi.python.org/pypi/python-radix

  Does not handle arbitrary bases. Converts int or int as str to str.

* numpy: http://docs.scipy.org/doc/numpy/reference/

  Converts int to str in bases between 2 and 36.


Packaging
---------
Downstream packagers, if incorporating testing into their packaging, are
encouraged to use only the tests in the test_deterministic module, to
avoid testing failures that may arise due to the non-deterministic behavior
of Hypothesis tests.
