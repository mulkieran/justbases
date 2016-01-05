Usage
=====

The library can be used in several ways.

NatDivision: Precise Division of Natural Numbers in any Base
------------------------------------------------------------
The method NatDivsion.division() takes a divisor, a dividend, and a base.
The divisor and dividend are numbers in the given base, represented as lists
of ints. The result is a tuple consisting of the integer portion of the
result, the non-repeating part after the radix, and the repeating part
after the radix. All parts of the result are in the given base and
represented as lists of ints.::

    >>> from justbases import NatDivision
    >>> NatDivision.division([1, 0], [1, 0, 0], 2)
    >>> ([1, 0], [], [])

The method NatDivision.undivision() does the inverse operation.
Note that these can only be considered as exact inverses if the arguments
to the division() method are mutually prime.::

    >>> NatDivision.undivision([1, 0], [], [], 2)
    >>> ([1], [1, 0])

Nats: Conversion of Natural Numbers between Arbitrary Bases
-----------------------------------------------------------
The method Nats.convert() takes a value as a list of ints in a given
base and returns a value as a list of ints in the target base.::

    >>> Nats.convert([3, 2], 10, 2)
    >>> [1, 0, 0, 0, 0, 0]

The methods convert_to_int() and convert_from_int() convert between
Python's internal integer representation and a representation of a
natural number in any base.::

    >>> from justbases import Nats
    >>> Nats.convert_from_int(32, 2)
    >>> [1, 0, 0, 0, 0, 0]

    >>> Nats.convert_to_int([3, 2], 10)
    >>> 32

Note that this is conversion of natural numbers, so all int values are
non-negative. Invoking convert_from_int() on a negative integer raises an
exception.

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

Rationals: Conversion of Rational Numbers between Arbitrary Bases
-----------------------------------------------------------------
A rational number can be converted to a Radix object and vice-versa.::

    >>> Rationals.convert_from_rational(Fraction(1, 3), 2)
    >>> .[0:1]_2 
    >>> Rationals.convert_to_rational(Radix(True, [], [], [0, 1], 2))
    >>> Fraction(1, 3)
    >>> Rationals.convert_from_rational(Fraction(60, 1), 60)
    >>> 1:0.[]_60

Radix objects can be converted between arbitrary bases.::

    >>> Rationals.convert(Radix(True, [], [], [0, 1], 2), 3)
    >>> .1[]_3

Rounding: Rounding Radix Values
-------------------------------
A radix can be rounded to any number of digits after the point.::

    >>> from justbases import RoundingMethods
    >>> Rounding.roundFractional(Radix(True, [], [], [0, 1], 2), 5, RoundingMethods.ROUND_UP)
    >>> .0:1:0:1:1[]_2
    >>> Rounding.roundFractional(Radix(True, [], [], [0, 1], 2), 5, RoundingMethods.ROUND_HALF_DOWN)
    >>> .0:1:0:1:0[]_2

Concrete Example: Geographic Coordinates 
----------------------------------------
Latitude and longitude are frequently expressed in degrees, minutes, and
seconds, using the base 60. Below is a simple exercise to translate
a given latitude into alternative formats.::

    >>> latitude = (42, 38, 0) # latitude measurement
    >>> latitude_rational = Fraction((((42 * 60) + 38) * 60), 60**2)
    >>> latitude_rational
    >>> Fraction(1279, 30) # latitude as a rational number
    >>> radix = Rationals.convert_from_rational(latitude_rational, 10)
    >>> radix
    >>> 4:2.6[3]_10
    >>> Rounding.roundFractional(radix, 2, RoundingMethods.ROUND_TO_ZERO)
    >>> 4:2.6:3[]_10
    >>> Rationals.convert(radix, 60)
    >>> 42.38[]_60
    >>> Rationals.convert(radix, 3600)
    >>> 42.2280[]_3600
