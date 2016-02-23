# Copyright (C) 2015 Anne Mulhern
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# Anne Mulhern <mulhern@cs.wisc.edu>

"""
Methods dealing with rationals.
"""
import itertools

from fractions import Fraction

from ._constants import RoundingMethods
from ._division import NatDivision
from ._errors import BasesAssertError
from ._errors import BasesInvalidOperationError
from ._errors import BasesValueError
from ._nats import Nats


class Rationals(object):
    """
    Methods to convert non-negative ints.
    """

    @classmethod
    def convert(cls, value, to_base):
        """
        Convert value from a base to a base.

        :param Radix value: the value to convert
        :param int to_base: base of result
        :returns: the conversion result
        :rtype: Radix of int
        :raises ConvertError: if to_base is less than 2
        """
        return cls.convert_from_rational(
           cls.convert_to_rational(value),
           to_base
        )

    @staticmethod
    def convert_to_rational(value):
        """
        Convert value to a rational.

        :param Radix value: the value to convert
        :returns: the conversion result
        :rtype: Rational
        :raises ConvertError: if from_base is less than 2

        Complexity: Uncalculated.
        """
        (denominator, numerator) = \
           NatDivision.undivision(
              value.integer_part,
              value.non_repeating_part,
              value.repeating_part,
              value.base
           )
        result = Fraction(
           Nats.convert_to_int(numerator, value.base),
           Nats.convert_to_int(denominator, value.base)
        )
        return result * (1 if value.positive else -1)

    @staticmethod
    def _reverse_rounding_method(method):
        """
        Reverse meaning of ``method`` between positive and negative.
        """
        if method is RoundingMethods.ROUND_UP:
            return RoundingMethods.ROUND_DOWN
        if method is RoundingMethods.ROUND_DOWN:
            return RoundingMethods.ROUND_UP
        if method is RoundingMethods.ROUND_HALF_UP:
            return RoundingMethods.ROUND_HALF_DOWN
        if method is RoundingMethods.ROUND_HALF_DOWN:
            return RoundingMethods.ROUND_HALF_UP
        if method in \
           (RoundingMethods.ROUND_TO_ZERO, RoundingMethods.ROUND_HALF_ZERO):
            return method
        raise BasesAssertError('unknown method')

    @classmethod
    def convert_from_rational(
       cls,
       value,
       to_base,
       precision=None,
       method=RoundingMethods.ROUND_DOWN
    ):
        """
        Convert rational value to a base.

        :param Rational value: the value to convert
        :param int to_base: base of result, must be at least 2
        :param precision: number of digits in total or None
        :type precision: int or NoneType
        :param method: rounding method
        :type method: element of RoundingMethods.METHODS()
        :returns: the conversion result
        :rtype: Radix
        :raises BasesValueError: if to_base is less than 2

        Complexity: Uncalculated.
        """
        if to_base < 2:
            raise BasesValueError(to_base, "to_base", "must be at least 2")

        if precision is not None and precision < 0:
            raise BasesValueError(precision, "precision", "must be at least 0")

        positive = True if value >= 0 else False
        div_method = method

        if positive is False:
            value = abs(value)
            div_method = cls._reverse_rounding_method(method)

        numerator = Nats.convert_from_int(value.numerator, to_base)
        denominator = Nats.convert_from_int(value.denominator, to_base)

        (integer_part, non_repeating_part, repeating_part) = \
           NatDivision.division(
              denominator,
              numerator,
              to_base,
              precision,
              div_method
           )

        result = Radix(
           positive,
           integer_part,
           non_repeating_part,
           repeating_part,
           to_base
        )

        if precision is not None:
            return Rounding.roundFractional(result, precision, method)
        else:
            return result

    @staticmethod
    def round_to_int(value, method):
        """
        Round ``value`` to an int according to ``method``.

        :param Rational value: the value to round
        :param method: the rounding method (of RoundingMethods.METHODS())

        :returns: rounded value
        :rtype: int

        Complexity: O(1)
        """
        # pylint: disable=too-many-return-statements
        if value.denominator == 1:
            return value.numerator

        int_value = int(value)
        if int_value < value:
            (lower, upper) = (int_value, int_value + 1)
        else:
            (lower, upper) = (int_value - 1, int_value)

        if method is RoundingMethods.ROUND_DOWN:
            return lower

        if method is RoundingMethods.ROUND_UP:
            return upper

        if method is RoundingMethods.ROUND_TO_ZERO:
            return upper if lower < 0 else lower

        delta = value - lower

        if method is RoundingMethods.ROUND_HALF_UP:
            return upper if delta >= Fraction(1, 2) else lower

        if method is RoundingMethods.ROUND_HALF_DOWN:
            return lower if delta <= Fraction(1, 2) else upper

        if method is RoundingMethods.ROUND_HALF_ZERO:
            if lower < 0:
                return upper if delta >= Fraction(1, 2) else lower
            else:
                return lower if delta <= Fraction(1, 2) else upper

        raise BasesValueError(method, "method")


class Radix(object):
    """
    An object containing information about a rational representation.

    Such values can not be ordered, but can be compared for equality.
    """
    # pylint: disable=too-few-public-methods

    @classmethod
    def _validate( # pylint: disable=too-many-arguments
        cls,
        positive, # pylint: disable=unused-argument
        integer_part,
        non_repeating_part,
        repeating_part,
        base
    ):
        """
        Check if radix is valid.

        :param bool positive: True if value is positive, otherwise False
        :param integer_part: the part on the left side of the radix
        :type integer_part: list of int
        :param non_repeating_part: non repeating part on left side
        :type non_repeating_part: list of int
        :param repeating_part: repeating part
        :type repeating_part: list of int
        :param int base: base of the radix, must be at least 2

        :returns: BasesValueError if invalid values
        :rtype: BasesValueError or NoneType

        Complexity: O(len(integer_part + non_repeating_part + repeating_part))
        """
        if any(x < 0 or x >= base for x in integer_part):
            return BasesValueError(
               integer_part,
               "integer_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in non_repeating_part):
            return BasesValueError(
               non_repeating_part,
               "non_repeating_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in repeating_part):
            return BasesValueError(
               repeating_part,
               "repeating_part",
               "values must be between 0 and %s" % base
            )
        if base < 2:
            return BasesValueError(base, "base", "must be at least 2")
        return None

    @classmethod
    def _repeat_length(cls, part):
        """
        The length of the repeated portions of ``part``.

        :param part: a number
        :type part: list of int
        :returns: the first index at which part repeats
        :rtype: int

        If part does not repeat, result is the length of part.

        Complexity: O(len(part)^2)
        """
        repeat_len = len(part)
        if repeat_len == 0:
            return repeat_len

        first_digit = part[0]
        limit = repeat_len // 2 + 1
        indices = (i for i in range(1, limit) if part[i] == first_digit)
        for index in indices:
            (quot, rem) = divmod(repeat_len, index)
            if rem == 0:
                first_chunk = part[0:index]
                if all(first_chunk == part[x:x + index] \
                   for x in range(index, quot * index, index)):
                    return index
        return repeat_len

    @classmethod
    def _canonicalize_fraction(cls, non_repeating, repeating):
        """
        If the same fractional value can be represented by stripping repeating
        part from ``non_repeating``, do it.

        :param non_repeating: non repeating part of fraction
        :type non_repeating: list of int
        :param repeating: repeating part of fraction
        :type repeating: list of int
        :returns: new non_repeating and repeating parts
        :rtype: tuple of list of int * list of int

        Complexity: O(len(non_repeating))
        """
        if repeating == []:
            return (non_repeating, repeating)

        repeat_len = len(repeating)

        # strip all exact matches:
        # * for [6, 1, 2, 1, 2], [1,2] end is 1
        # * for [1, 2, 1, 2], [1,2] end is 0
        # * for [6, 2, 1, 2], [1,2] end is 2
        indices = range(len(non_repeating), -1, -repeat_len)
        end = next( # pragma: no cover
           i for i in indices if non_repeating[(i - repeat_len):i] != repeating
        )

        # for remaining, find partial match and shift repeating
        # * for [6, 2, 1, 2], [1, 2] initial end is 2, result is [6], [2, 1]
        indices = range(min(repeat_len - 1, end), 0, -1)
        index = next(
           (i for i in indices \
              if repeating[-i:] == non_repeating[(end-i):end]),
           0
        )
        return (
           non_repeating[:(end - index)],
           repeating[-index:] + repeating[:-index]
        )

    def __init__( # pylint: disable=too-many-arguments
        self,
        positive,
        integer_part,
        non_repeating_part,
        repeating_part,
        base,
        validate=True,
        canonicalize=True
    ):
        """
        Initializer.

        :param bool positive: True if value is positive, otherwise False
        :param integer_part: the part on the left side of the radix
        :type integer_part: list of int
        :param non_repeating_part: non repeating part on left side
        :type non_repeating_part: list of int
        :param repeating_part: repeating part
        :type repeating_part: list of int
        :param int base: base of the radix, must be at least 2
        :param bool validate: if True, validate the arguments
        :param bool canonicalize: if True, canonicalize

        Validation and canonicalization are expensive and may be omitted.

        Complexity: polynomial in number of digits if canonicalize is True,
        linear if validate is True, otherwise constant time
        """
        if validate:
            error = self._validate(
               positive,
               integer_part,
               non_repeating_part,
               repeating_part,
               base
            )
            if error is not None:
                raise error

        if canonicalize:
            if all(x == 0 for x in integer_part):
                integer_part = []

            if all(x == 0 for x in repeating_part):
                repeating_part = []

            if integer_part == [] and repeating_part == [] and \
               all(x == 0 for x in non_repeating_part):
                positive = True

            repeating_part = repeating_part[0:self._repeat_length(repeating_part)]
            (non_repeating_part, repeating_part) = \
                self._canonicalize_fraction(non_repeating_part, repeating_part)

        self.positive = positive
        self.base = base
        self.integer_part = integer_part
        self.non_repeating_part = non_repeating_part
        self.repeating_part = repeating_part

    def __str__(self):
        return ('' if self.positive else '-') + \
           ':'.join(str(x) for x in self.integer_part) + \
           '.' + \
           ':'.join(str(x) for x in self.non_repeating_part) + \
           '[%s]' % ':'.join(str(x) for x in self.repeating_part) + \
           '_' + \
           str(self.base)
    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Radix):
            raise BasesInvalidOperationError("!=", other)
        return self.positive == other.positive and \
           self.integer_part == other.integer_part and \
           self.non_repeating_part == other.non_repeating_part and \
           self.repeating_part == other.repeating_part and \
           self.base == other.base

    def __ne__(self, other):
        if not isinstance(other, Radix):
            raise BasesInvalidOperationError("!=", other)
        return self.positive != other.positive or \
           self.integer_part != other.integer_part or \
           self.non_repeating_part != other.non_repeating_part or \
           self.repeating_part != other.repeating_part or \
           self.base != other.base

    def __lt__(self, other):
        raise BasesInvalidOperationError("<")

    def __gt__(self, other):
        raise BasesInvalidOperationError(">")

    def __le__(self, other):
        raise BasesInvalidOperationError("<=")

    def __ge__(self, other):
        raise BasesInvalidOperationError(">=")


class Rounding(object):
    """
    Rounding of radix objects.
    """
    # pylint: disable=too-few-public-methods


    @staticmethod
    def _conditional_toward_zero(method, positive):
        """
        Whether to round toward zero.

        :param method: rounding method
        :type method: element of RoundingMethods.METHODS()
        :bool positive: if value is positive

        Complexity: O(1)
        """
        return method is RoundingMethods.ROUND_HALF_ZERO or \
           (method is RoundingMethods.ROUND_HALF_DOWN and positive) or \
           (method is RoundingMethods.ROUND_HALF_UP and not positive)

    @staticmethod
    def _increment(positive, integer_part, non_repeating_part, base):
        """
        Return an increment radix.

        :param bool positive: positive if Radix is positive
        :param integer_part: the integer part
        :type integer_part: list of int
        :param non_repeating_part: the fractional part
        :type non_repeating_part: list of int
        :param int base: the base

        :returns: a Radix object with ``non_repeating_part`` rounded up
        :rtype: Radix

        Complexity: O(len(non_repeating_part + integer_part)
        """
        (carry, non_repeating_part) = \
           Nats.carry_in(non_repeating_part, 1, base)
        (carry, integer_part) = \
           Nats.carry_in(integer_part, carry, base)
        return Radix(
           positive,
           integer_part if carry == 0 else [carry] + integer_part,
           non_repeating_part,
           [],
           base,
           False
        )

    @classmethod
    def roundFractional(cls, value, precision, method):
        """
        Round to precision as number of digits after radix.

        :param Radix value: value to round
        :param int precision: number of digits in total
        :param method: rounding method

        Precondition: Radix is valid and canonical

        Complexity: O(len(components))
        """
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-branches

        if precision < 0:
            raise BasesValueError(
               precision,
               "precision",
               "must be at least 0"
            )

        if method not in RoundingMethods.METHODS():
            raise BasesValueError(
               method,
               "method",
               "must be one of RoundingMethod.METHODS()"
            )

        digits = itertools.chain(
           value.non_repeating_part,
           itertools.cycle(value.repeating_part)
        )
        non_repeating_part = list(itertools.islice(digits, 0, precision))
        non_repeating_part += (precision - len(non_repeating_part)) * [0]

        # pylint: disable=too-many-boolean-expressions
        if method is RoundingMethods.ROUND_TO_ZERO or \
           (all(x == 0 for x in value.non_repeating_part[precision:]) and \
            len(value.repeating_part) == 0) or \
           (method is RoundingMethods.ROUND_DOWN and value.positive) or \
           (method is RoundingMethods.ROUND_UP and not value.positive):
            return Radix(
               value.positive,
               value.integer_part,
               non_repeating_part,
               [],
               value.base,
               False
            )

        if method in (
           RoundingMethods.ROUND_DOWN,
           RoundingMethods.ROUND_UP
        ):
            return cls._increment(
               value.positive,
               value.integer_part,
               non_repeating_part,
               value.base
            )

        non_repeating_remainder = value.non_repeating_part[precision:]
        if non_repeating_remainder == []:
            repeating_part = \
               list(itertools.islice(digits, len(value.repeating_part)))
        else:
            repeating_part = value.repeating_part[:]
        remainder = \
            Rationals.convert_to_rational(
               Radix(
                  True,
                  [],
                  non_repeating_remainder,
                  repeating_part,
                  value.base,
                  False
               )
            )
        middle = Fraction(1, 2)
        if remainder < middle:
            return Radix(
               value.positive,
               value.integer_part,
               non_repeating_part,
               [],
               value.base,
               False
            )
        elif remainder > middle:
            return cls._increment(
               value.positive,
               value.integer_part,
               non_repeating_part,
               value.base
            )
        else:
            if cls._conditional_toward_zero(method, value.positive):
                return Radix(
                   value.positive,
                   value.integer_part,
                   non_repeating_part,
                   [],
                   value.base,
                   False
                )
            else:
                return cls._increment(
                   value.positive,
                   value.integer_part,
                   non_repeating_part,
                   value.base
                )

        raise BasesAssertError() # pragma: no cover
