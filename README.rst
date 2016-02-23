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

