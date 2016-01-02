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
A type for holding a non-integer rational.
"""

from fractions import Fraction

from ._constants import RoundingMethods
from ._errors import ConvertValueError
from ._nats import Nats


class Radix(object):
    """
    An object containing information about a rational representation.
    """
    # pylint: disable=too-few-public-methods

    def __init__( # pylint: disable=too-many-arguments
        self,
        positive,
        integer_part,
        non_repeating_part,
        repeating_part,
        base
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
        """
        self.positive = positive

        if any(x < 0 or x >= base for x in integer_part):
            raise ConvertValueError(
               integer_part,
               "integer_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in non_repeating_part):
            raise ConvertValueError(
               non_repeating_part,
               "non_repeating_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in repeating_part):
            raise ConvertValueError(
               repeating_part,
               "repeating_part",
               "values must be between 0 and %s" % base
            )
        if base < 2:
            raise ConvertValueError(base, "base", "must be at least 2")

        self.base = base
        self.integer_part = integer_part
        self.non_repeating_part = non_repeating_part
        self.repeating_part = repeating_part

    def __str__(self):
        return ('' if self.positive else '-') + \
           ''.join(str(x) for x in self.integer_part) + \
           '.' + \
           ''.join(str(x) for x in self.non_repeating_part) + \
           '[%s]' % ''.join(str(x) for x in self.repeating_part) + \
           '_' + \
           str(self.base)
    __repr__ = __str__


class Rounding(object):
    """
    Rounding of radix objects.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def _down(positive):
        """
        Amount to add if rounding down.

        :param bool positive: True if the actual value is positive, else False
        :returns: the increment value
        :rtype: int
        """
        return 0 if positive else 1

    @staticmethod
    def _up(positive):
        """
        Amount to add if round up.

        :param bool positive: True if the actual value is positive, else False
        :returns: the increment value
        :rtype: int
        """
        return 1 if positive else 0

    @classmethod
    def _increment_conditional(cls, positive, method, middle, breaker):
        """
        The amount by which to increment if incrementing at all.
        Note that the number being operated on is always non-negative.

        :param bool positive: if the number is positive
        :param method: rounding method, HALF kind
        :param Fraction middle: the middle value
        :type middle: Fraction or NoneType
        :param breaker: the non-middle value found
        :type breaker: int or NoneType

        :returns: amount by which to increment
        :rtype: int (1 or 0)
        """
        if method is RoundingMethods.ROUND_HALF_DOWN:
            if breaker is None or breaker <= middle:
                return 0
            else:
                return cls._up(positive)
        if method is RoundingMethods.ROUND_HALF_UP:
            if breaker is None or breaker >= middle:
                return cls._up(positive)
            else:
                return 0
        if method is RoundingMethods.ROUND_HALF_ZERO:
            if breaker is None or breaker <= middle:
                return 0
            else:
                return 1
        raise ConvertValueError(
            method,
            "method",
            "unknown method"
        )

    @classmethod
    def _increment_unconditional(cls, positive, method):
        """
        The amount by which to increment if incrementing at all.
        Note that the number being operated on is always non-negative.

        :param bool positive: if the number is positive
        :param method: rounding method, absolute kind

        :returns: amount by which to increment
        :rtype: int (1 or 0)
        """
        if method is RoundingMethods.ROUND_DOWN:
            return cls._down(positive)
        if method is RoundingMethods.ROUND_TO_ZERO:
            return 0
        if method is RoundingMethods.ROUND_UP:
            return cls._up(positive)
        raise ConvertValueError(
            method,
            "method",
            "unknown method"
        )

    @staticmethod
    def _tieBreaker(
       middle,
       start,
       integer_part,
       non_repeating_part,
       repeating_part
    ):
        """
        Find the first tie-breaking digit in the number.

        :param Fraction middle: the middle value for the base
        :param int start: where to start looking
        :param integer_part: the integer part of the number
        :type integer_part: list of int
        :param non_repeating_part: the integer part of the number
        :type non_repeating_part: list of int
        :param repeating_part: the integer part of the number
        :type repeating_part: list of int
        :returns: first tie breaking digit or None if none found
        :rtype: int or NoneType
        """
        number = integer_part + non_repeating_part + repeating_part
        if start > len(number):
            start = (start - len(number)) % len(repeating_part)
            value = repeating_part[start:] + repeating_part[:start]
        else:
            value = number[start:]
        return next((x for x in value if x != middle), None)

    @staticmethod
    def _exact(
       start,
       integer_part,
       non_repeating_part,
       repeating_part
    ):
        """
        Whether the value is exact.

        :returns: True if exact, otherwise False
        :rtype: bool
        """
        number = integer_part + non_repeating_part
        return all(x == 0 for x in number[start:]) and \
           all(x == 0 for x in repeating_part)

    @classmethod
    def _increment(
       cls,
       positive,
       method,
       middle,
       start,
       integer_part,
       non_repeating_part,
       repeating_part
    ): # pylint: disable=too-many-arguments
        """
        Amount to increment.

        :returns: the amount to increment
        :rtype: int
        """
        if cls._exact(start, integer_part, non_repeating_part, repeating_part):
            return 0

        if method in RoundingMethods.CONDITIONAL_METHODS():
            breaker = cls._tieBreaker(
               middle,
               start,
               integer_part,
               non_repeating_part,
               repeating_part
            )
            return cls._increment_conditional(positive, method, middle, breaker)
        else:
            return cls._increment_unconditional(positive, method)

    @staticmethod
    def _add(part, base, increment):
        """
        Add ``increment`` to ``part`` in ``base``.

        :param part: the part of a Radix to be added.
        :type part: list of int
        :param int base: the base
        :param int increment: the increment

        :returns: result of addition, including a carry digit
        :rtype: tuple of int * list of int
        """
        length = len(part)
        part = Nats.convert_from_int(
           Nats.convert_to_int(part, base) + increment,
           base
        )

        if len(part) < length:
            return (0, (length - len(part)) * [0] + part)

        if len(part) > length:
            return (part[0], part[1:])
        else:
            return (0, part)

    @staticmethod
    def _expandFraction(value, precision):
        """
        Expand fractional part of ``value`` to ``precision``.

        :param Radix value: the value
        :param int precision: precision
        :returns: the value of the expanded fractional part
        :rtype: list of int
        """
        result = value.non_repeating_part[:precision]
        precision = precision - len(value.non_repeating_part)
        if precision <= 0:
            return result

        if value.repeating_part == []:
            return result + [0] * precision

        (quot, rem) = divmod(precision, len(value.repeating_part))
        return result + \
           (quot * value.repeating_part) + value.repeating_part[:rem]


    @classmethod
    def roundFractional(cls, value, precision, method):
        """
        Round to precision as number of digits after radix.

        :param Radix value: value to round
        :param int precision: number of digits in total
        :param method: rounding method
        """

        if precision < 0:
            raise ConvertValueError(
               precision,
               "precision",
               "must be at least 0"
            )

        middle = Fraction(value.base, 2)

        increment = cls._increment(
           value.positive,
           method,
           middle,
           precision + len(value.integer_part),
           value.integer_part,
           value.non_repeating_part,
           value.repeating_part
        )

        carry = 0
        integer_part = value.integer_part
        non_repeating_part = cls._expandFraction(value, precision)

        (carry, non_repeating_part) = \
           cls._add(non_repeating_part, value.base, increment)

        padding = (precision - len(non_repeating_part)) * [0]
        non_repeating_part += padding

        if carry != 0:
            (carry, integer_part) = \
               cls._add(integer_part, value.base, carry)
        if carry != 0:
            integer_part = [carry] + integer_part

        return Radix(
           value.positive,
           integer_part,
           non_repeating_part,
           [],
           value.base
        )
