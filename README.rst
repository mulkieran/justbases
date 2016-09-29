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

__str__ method
--------------
This method does not constitute part of the justbases public API. It is meant
to be read by humans, not machines, and may change at any time.

Related Packages
----------------

* allyourbase: https://pypi.python.org/pypi/allyourbase

  Converts a variety of numeric types to str in arbitrary bases.
  Does not require one character to digit encoding, uses a digit separator.
  Requires rounding, does not do precise conversion, but does do
  conversion to any specified precision.

* baseconvert: https://pypi.python.org/pypi/baseconvert

  Converts between arbitrary bases.
  Seems to use a heuristic for identifying sequences of repeating digits,
  which it then encloses in square brackets, rather than constructing the
  correct sequence of repeating digits by division.

* decimalfp: https://pypi.python.org/pypi/decimalfp

  Seems to be an alternative to the python Decimal class.

* python-baseconv: https://pypi.python.org/pypi/python-baseconv

  Converts an int to a string using a one character to digit encoding.
  Also converts in the opposite direction.
  Does not handle arbitrary rationals and does not really handle conversion to
  large bases, e.g., 1024, as such conversion would require 1024 distinct
  characters.

* python-radix: https://pypi.python.org/pypi/python-radix

  Does not handle arbitrary bases. Converts natural number or natural number
  represented as a str to a str representation of the result.

* python-nicefloat: https://pypi.python.org/pypi/python-nicefloat

  Represents a floating point number s.t. if f is any floating point number,
  float(nicefloat(f)) == f. This property does not hold for float(str(f)),
  but does for float(repr(f)). The result of nicefloat generally has fewer
  characters than that of repr.

* numpy: http://docs.scipy.org/doc/numpy/reference/

  Converts int to str in bases between 2 and 36.

PRs
---

Some related packages offer features that justbases does not, like a
user-friendly API or a CLI. In many cases, these packages can be adapted
to make use of justbases, ensuring correctness, increasing their usefulness,
and at the same time, offering a higher-level interaction with
justbases.

The following packages have outstanding PRs to introduce a dependency on
justbases:

* baseconvert: https://pypi.python.org/pypi/baseconvert

  PR: https://github.com/squdle/baseconvert/pull/1

* python-radix: https://github.com/valbub/python-radix

  PR: https://github.com/valbub/python-radix/pull/1

  PR: https://github.com/valbub/python-radix/pull/2
