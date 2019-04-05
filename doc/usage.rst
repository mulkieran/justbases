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
    >>> ([], [], [], Fraction(-1, 3))

The default rounding method is round down, but other rounding methods
may be specified. ::

    >>> NatDivision.division([3], [1], 10, 0, RoundingMethods.ROUND_UP)
    >>> ([1], [], [], Fraction(2, 3))

The final element in the tuple indicates the difference between the rounded
value and the original value as the ratio of the difference between the two
values to the ULP.

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

It is possible to round a natural number using any of the defined rounding
methods by specifying a negative precision to the roundTo() method, as::

   >>> Nats.roundTo([1, 1, 1], 10, -1, RoundingMethods.ROUND_DOWN)
   ([1, 1, 0], Fraction(-1, 10))

The two parts of the result indicate the rounded value, and the ratio of the
difference between the rounded value and the actual value to the ULP.

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
    >>> Radix(-1, [1], [2], [1], 10)
    >>> -1.2[1]_10
    >>> Radix(1, [12, 13], [4], [], 16)
    >>> 12:13.4[]_16

Note that the number after the underscore represents the base, and the
digits within square brackets represent the repeating portion of the
number. Individual digits in a decimal representation require a separator,
here a ':'. This approach supports arbitrary bases.

The Radix constructor validates and canonicalizes the Radix.
Validation ensures that the digits are within the appropriate range
for the given base, and other digits. Canonicalization ensures a canonical
representation for equivalent Radix values. For example, it reduces
the repeating part to the smallest possible. ::

    >>> Radix(1, [], [], [1, 0, 1, 0], 2)
    >>> .[1:0]_2

Canonicalization and validation are expensive, and may be omitted when
unnecessary, for example, when an algorithm is known to yield a canonical
value or when operations, such as ==, which require canonicalization for
their correctness, are not anticipated. ::

    >>> Radix(1, [], [], [1, 0, 1, 0], 2, canonicalize=False)
    >>> .[1:0:1:0]_2

Although canonicalized Radix objects may be compared for
equality, they can not be ordered. To compare the values of two Radix
objects convert each to a Rational and compare the resulting values.


Radices: Conversion of a Rational Number to a Radix
---------------------------------------------------
A rational number can be converted to a Radix object and vice-versa.
The first element of the pair is the result, the second indicates the
relation of the result to the actual value. ::

    >>> Radices.from_rational(Fraction(1, 3), 2)
    (Radix(1,[],[],[0, 1],2), 0)
    >>> Radix(1, [], [], [0, 1], 2).as_rational()
    Fraction(1, 3)
    >>> Radices.from_rational(Fraction(60, 1), 60)
    (Radix(1,[1, 0],[],[],60), 0)

Radix objects can be converted between arbitrary bases. ::

    >>> Radix(1, [], [], [0, 1], 2).in_base(3)
    Radix(1,[],[1],[],3)

Rationals: Rounding Rationals
----------------------------

A rational can be rounded to an int according to a specified method. ::

    >>> Rationals.round_to_int(Fraction(7, 3), RoundingMethods.ROUND_DOWN)
    >>> (2, Fraction(-1, 3))

Rounding Radix Values
-------------------------------
A radix can be rounded to any number of digits after the point.
The second element of the pair indicates the direction of rounding. ::

    >>> from justbases import RoundingMethods
    >>> Radix(1, [], [], [0, 1], 2).rounded(5, RoundingMethods.ROUND_UP)
    (Radix(1,[],[0, 1, 0, 1, 1],[],2), Fraction(1, 3))
    >>> Radix(1, [], [], [0, 1], 2).rounded(5, RoundingMethods.ROUND_HALF_DOWN)
    (Radix(1,[],[0, 1, 0, 1, 1],[],2), Fraction(1, 3))

If the goal is to obtain a radix value from a rounded rational quantity it is
more efficient to use Radices.from_rational() with precision and
method arguments set. ::

    >>> Radices.from_rational(Fraction(1, 3), 2, 1, RoundingMethods.ROUND_UP)
    (Radix(1,[],[1],[],2), Fraction(1, 3))


Display
-------
Radix.getString() returns a string representing a Radix object. The form of
this string can be modified using the config parameter. The justbases-gui
library is useful for experimenting with the different configuration options,
which control such things as the choice of representation for digits larger
than 9, whether or not to strip trailing zeros, and so forth. Consult the
justbases-gui documentation for its usage.


Concrete Example: Geographic Coordinates
----------------------------------------
Latitude and longitude are frequently expressed in degrees, minutes, and
seconds, using the base 60. Below is a simple exercise to translate
a given latitude into alternative formats. ::

    >>> latitude = (42, 38, 0) # latitude measurement
    >>> latitude_rational = Fraction((((42 * 60) + 38) * 60), 60**2)
    >>> latitude_rational
    Fraction(1279, 30) # latitude as a rational number
    >>> (radix, _) = Radices.from_rational(latitude_rational, 10)
    >>> radix
    Radix(1,[4, 2],[6],[3],10)
    >>> radix.rounded(2, RoundingMethods.ROUND_TO_ZERO)
    (Radix(1,[4, 2],[6, 3],[],10), Fraction(-1, 3)
    >>> radix.in_base(60)
    Radix(1,[42],[38],[],60)
    >>> radix.in_base(3600)
    Radix(1,[42],[2280],[],3600)
