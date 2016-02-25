Usage
=====

The library can be used in several ways.

NatDivision: Precise Division of Natural Numbers in any Base
------------------------------------------------------------
The method NatDivision.division() takes a divisor, a dividend, and a base.
The divisor and dividend are numbers in the given base, represented as lists
of ints. The result is a tuple consisting of the integer portion of the
value, the non-repeating part after the radix, the repeating part
after the radix and a flag indicating whether the value represented is
greater than, less than, or equal to the actual result.

All parts of the value are in the given base and represented as lists
of ints. ::

    >>> from justbases import NatDivision
    >>> NatDivision.division([1, 0], [1, 0, 0], 2)
    >>> ([1, 0], [], [], 0)

The method NatDivision.undivision() does the inverse operation.
Note that these can only be considered as exact inverses if the arguments
to the division() method are mutually prime. ::

    >>> NatDivision.undivision([1, 0], [], [], 2)
    >>> ([1], [1, 0])

It is allowed to specify a precision and a rounding method to the division()
method, for efficiency. If the precision is greater than the number of
digits in the non-repeating and repeating parts, the effect is the same
as if no precision were specified. If the precision is less than the length
of these two parts combined, then the part of the result that represents
the repeating part is guaranteed to be empty. ::

    >>> NatDivision.division([3], [1], 10)
    >>> ([], [], [3], 0)

    >>> NatDivision.division([3], [1], 10, 1)
    >>> ([], [], [3], 0)

    >>> NatDivision.division([3], [1], 10, 0)
    >>> ([], [], [], -1)

The default rounding method is round down, but other rounding methods
may be specified. ::

    >>> NatDivision.division([3], [1], 10, 0, RoundingMethods.ROUND_UP)
    >>> ([1], [], [], 1)

If the value of the expression is greater than the result of the
computation, the last element in the tuple is a 1, if less, -1, and, if
equal, 0.

Nats: Conversion of Natural Numbers between Arbitrary Bases
-----------------------------------------------------------
The method Nats.convert() takes a value as a list of ints in a given
base and returns a value as a list of ints in the target base. ::

    >>> Nats.convert([3, 2], 10, 2)
    >>> [1, 0, 0, 0, 0, 0]

The methods convert_to_int() and convert_from_int() convert between
Python's internal integer representation and a representation of a
natural number in any base. ::

    >>> from justbases import Nats
    >>> Nats.convert_from_int(32, 2)
    >>> [1, 0, 0, 0, 0, 0]

    >>> Nats.convert_to_int([3, 2], 10)
    >>> 32

Note that this is conversion of natural numbers, so all int values are
non-negative. Invoking convert_from_int() on a negative integer raises an
exception.

It is also possible to peform an add operation of a single digit to
a number in any base. ::

    >>> Nats.carry_in([1, 1], 1, 2)
    >>> (1, [0, 0])

The result has two parts: the carry-out digit and the value. The result
value has the same number of digits as the parameter value.


Radix: Non-fractional Representation of a Rational Number
---------------------------------------------------------
A class which represents a rational number as
  * a sign
  * an integer part
  * a non-repeating part
  * a repeating part
  * a base

::

    >>> from justbases import Radix
    >>> Radix(False, [1], [2], [1], 10)
    >>> -1.2[1]_10
    >>> Radix(True, [12, 13], [4], [], 16)
    >>> 12:13.4[]_16

Note that the number after the underscore represents the base, and the
digits within square brackets represent the repeating portion of the
number. Individual digits, in a decimal representation, are separated by
':''s. This approach supports arbitrary bases.

The Radix constructor validates and canonicalizes the Radix.
Validation ensures that the digits are within the appropriate range
for the given base, and other digits. Canonicalization ensures a canonical
representation for equivalent Radix values. For example, it reduces
the repeating part to the smallest possible. ::

    >>> Radix(True, [], [], [1, 0, 1, 0], 2)
    >>> .[1:0]_2

Canonicalization and validation are expensive, and may be omitted when
unnecessary, for example, when an algorithm is known to yield a canonical
value or when operations, such as ==, which require canonicalization for
their correctness, are not anticipated. ::

    >>> Radix(True, [], [], [1, 0, 1, 0], 2, canonicalize=False)
    >>> .[1:0:1:0]_2

Although canonicalized Radix objects may be compared for
equality, they can not be ordered. To compare the values of two Radix
objects convert each to a Rational and compare the resulting values.


Rationals: Conversion of Rational Numbers between Arbitrary Bases
-----------------------------------------------------------------
A rational number can be converted to a Radix object and vice-versa.
The first element of the pair is the result, the second indicates the
relation of the result to the actual value. ::

    >>> Rationals.convert_from_rational(Fraction(1, 3), 2)
    >>> (.[0:1]_2, 0)
    >>> Rationals.convert_to_rational(Radix(True, [], [], [0, 1], 2))
    >>> Fraction(1, 3)
    >>> Rationals.convert_from_rational(Fraction(60, 1), 60)
    >>> (1:0.[]_60, 0)

Radix objects can be converted between arbitrary bases. ::

    >>> Rationals.convert(Radix(True, [], [], [0, 1], 2), 3)
    >>> .1[]_3

Rounding: Rounding Rationals
----------------------------

A rational can be rounded to an int according to a specified method. ::

    >>> Rationals.round_to_int(Fraction(7, 3), RoundingMethods.ROUND_DOWN)
    >>> 2

Rounding: Rounding Radix Values
-------------------------------
A radix can be rounded to any number of digits after the point.
The second element of the pair indicates the direction of rounding. ::

    >>> from justbases import RoundingMethods
    >>> Rounding.roundFractional(Radix(True, [], [], [0, 1], 2), 5, RoundingMethods.ROUND_UP)
    >>> (.0:1:0:1:1[]_2, 1)
    >>> Rounding.roundFractional(Radix(True, [], [], [0, 1], 2), 5, RoundingMethods.ROUND_HALF_DOWN)
    >>> (.0:1:0:1:0[]_2, -1)

If the goal is to obtain a radix value from a rounded rational quantity it is
more efficient to use Rationals.convert_from_rational() with precision and
method arguments set. ::

    >>> Rationals.convert_from_rational(Fraction(1, 3), 2, 1, RoundingMethods.ROUND_UP)
    >>> (.1[]_2, 1)

Concrete Example: Geographic Coordinates
----------------------------------------
Latitude and longitude are frequently expressed in degrees, minutes, and
seconds, using the base 60. Below is a simple exercise to translate
a given latitude into alternative formats. ::

    >>> latitude = (42, 38, 0) # latitude measurement
    >>> latitude_rational = Fraction((((42 * 60) + 38) * 60), 60**2)
    >>> latitude_rational
    >>> Fraction(1279, 30) # latitude as a rational number
    >>> (radix, _) = Rationals.convert_from_rational(latitude_rational, 10)
    >>> radix
    >>> 4:2.6[3]_10
    >>> Rounding.roundFractional(radix, 2, RoundingMethods.ROUND_TO_ZERO)
    >>> (4:2.6:3[]_10, -1)
    >>> Rationals.convert(radix, 60)
    >>> 42.38[]_60
    >>> Rationals.convert(radix, 3600)
    >>> 42.2280[]_3600
