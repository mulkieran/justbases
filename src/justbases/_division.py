# Copyright (C) 2015 - 2019 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>
# Other Authors: Anne Mulhern <mulhern@cs.wisc.edu>

"""
Long division in any bases.
"""

from __future__ import absolute_import

import fractions
import itertools

from ._constants import RoundingMethods
from ._errors import BasesValueError
from ._nats import Nats


class NatDivision:
    """
    Methods for division in arbitrary bases.
    """

    @classmethod
    def _round(
        cls, quotient, divisor, remainder, base, method=RoundingMethods.ROUND_DOWN
    ):
        """
        Round the quotient.

        :param quotient: current quotient
        :type quotient: list of int
        :param int divisor: the divisor
        :param int remainder: the remainder
        :param int base: the base
        :param method: the rounding method
        :raises BasesValueError:

        :returns: carry-out digit, non_repeating and repeating parts
        :rtype: tuple of int * list of int * list of int * int

        Complexity: O(len(quotient))
        """
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-arguments
        if method not in RoundingMethods.METHODS():
            raise BasesValueError(
                method, "method", "must be one of RoundingMethods.METHODS"
            )

        if remainder == 0:  # pragma: no cover
            return (0, quotient, [], 0)

        if method is RoundingMethods.ROUND_DOWN:
            return (0, quotient, [], -1)
        if method is RoundingMethods.ROUND_TO_ZERO:
            return (0, quotient, [], -1)
        if method is RoundingMethods.ROUND_UP:
            (carry, quotient) = Nats.carry_in(quotient, 1, base)
            return (carry, quotient, [], 1)

        remainder = fractions.Fraction(remainder, divisor)
        middle = fractions.Fraction(base, 2)
        if remainder < middle:
            return (0, quotient, [], -1)
        if remainder > middle:
            (carry, quotient) = Nats.carry_in(quotient, 1, base)
            return (carry, quotient, [], 1)

        if method is RoundingMethods.ROUND_HALF_UP:
            (carry, quotient) = Nats.carry_in(quotient, 1, base)
            return (carry, quotient, [], 1)
        if method in (RoundingMethods.ROUND_HALF_DOWN, RoundingMethods.ROUND_HALF_ZERO):
            return (0, quotient, [], -1)

        raise BasesValueError(  # pragma: no cover
            method, "method", "must be one of RoundingMethods.METHODS"
        )

    @staticmethod
    def _divide(divisor, remainder, quotient, remainders, base, precision=None):
        """
        Given a divisor and dividend, continue until precision in is reached.

        :param int divisor: the divisor
        :param int remainder: the remainder
        :param int base: the base
        :param precision: maximum number of fractional digits to compute
        :type precision: int or NoneType

        :returns: the remainder
        :rtype: int

        ``quotient`` and ``remainders`` are set by side effects

        Complexity: O(precision) if precision is not None else O(divisor)
        """
        # pylint: disable=too-many-arguments

        indices = itertools.count() if precision is None else range(precision)

        for _ in indices:
            if remainder == 0 or remainder in remainders:
                break
            remainders.append(remainder)
            (quot, rem) = divmod(remainder, divisor)
            quotient.append(quot)
            if quot > 0:
                remainder = rem * base
            else:
                remainder = remainder * base
        return remainder

    @classmethod
    def _fractional_division(
        cls, divisor, remainder, base, precision=None, method=RoundingMethods.ROUND_DOWN
    ):
        """
        Get the repeating and non-repeating part.

        :param int divisor: the divisor
        :param int remainder: the remainder
        :param int base: the base
        :param precision: maximum number of fractional digits
        :type precision: int or NoneType
        :param method: rounding method
        :type method: element of RoundignMethods.METHODS

        :returns: carry-out digit, non_repeating and repeating parts
        :rtype: tuple of int * list of int * list of int * int

        :raises BasesValueError:

        Complexity: O(precision) if precision is not None else O(divisor)
        """
        # pylint: disable=too-many-arguments
        quotient = []
        remainders = []
        remainder = cls._divide(
            divisor, remainder * base, quotient, remainders, base, precision
        )

        if remainder == 0:
            return (0, quotient, [], 0)
        if remainder in remainders:
            start = remainders.index(remainder)
            return (0, quotient[:start], quotient[start:], 0)
        return cls._round(quotient, divisor, remainder, base, method)

    @staticmethod
    def _division(divisor, dividend, remainder, base):
        """
        Get the quotient and remainder

        :param int divisor: the divisor
        :param dividend: the divident
        :type dividend: sequence of int
        :param int remainder: initial remainder
        :param int base: the base

        :returns: quotient and remainder
        :rtype: tuple of (list of int) * int

        Complexity: O(log_{divisor}(quotient))
        """
        quotient = []
        for value in dividend:
            remainder = remainder * base + value
            (quot, rem) = divmod(remainder, divisor)
            quotient.append(quot)
            if quot > 0:
                remainder = rem
        return (quotient, remainder)

    @classmethod
    def division(
        cls, divisor, dividend, base, precision=None, method=RoundingMethods.ROUND_DOWN
    ):
        """
        Division of natural numbers.

        :param divisor: the divisor
        :type divisor: list of int
        :param dividend: the dividend
        :type dividend: list of int
        :param precision: maximum number of fractional digits
        :type precision: int or NoneType
        :param method: rounding method
        :type method: element of RoundignMethods.METHODS
        :returns: the result
        :rtype: tuple of list of int * list of int * list of int * int
        :raises ConvertError: on invalid values

        The last value in the result indicates the relationship of the
        result to the actual value. If 0, it is the same, if 1, greater,
        if -1, less.

        Complexity: Uncalculated
        """
        # pylint: disable=too-many-arguments

        if base < 2:
            raise BasesValueError(base, "base", "must be at least 2")

        if precision is not None and precision < 0:
            raise BasesValueError(precision, "precision", "must be at least 0")

        if any(x < 0 or x >= base for x in divisor):
            raise BasesValueError(
                divisor, "divisor", "for all elements, e, 0 <= e < base required"
            )

        if any(x < 0 or x >= base for x in dividend):
            raise BasesValueError(
                divisor, "divisor", "for all elements, e, 0 <= e < base required"
            )

        if all(x == 0 for x in divisor):
            raise BasesValueError(divisor, "divisor", "must be greater than 0")

        divisor = Nats.convert_to_int(divisor, base)

        (integer_part, rem) = cls._division(divisor, dividend, 0, base)
        (
            carry,
            non_repeating_part,
            repeating_part,
            relation,
        ) = cls._fractional_division(divisor, rem, base, precision, method)

        (carry, integer_part) = Nats.carry_in(integer_part, carry, base)

        return (
            list(itertools.dropwhile(lambda x: x == 0, [carry] + integer_part)),
            non_repeating_part,
            repeating_part,
            relation,
        )

    @classmethod
    def undivision(cls, integer_part, non_repeating_part, repeating_part, base):
        """
        Find divisor and dividend that yield component parts.

        :param integer_part: the integer part
        :type integer_part: list of int
        :param non_repeating_part: the non_repeating_part
        :type non_repeating_part: list of int
        :param repeating_part: the repeating part
        :type repeating_part: list of int
        :param int base: the base

        :returns: divisor and dividend in lowest terms
        :rtype: tuple of list of int * list of int

        Complexity: O(len(non_repeating_part + repeating_part + integer_part))
        """
        if base < 2:
            raise BasesValueError(base, "base", "must be at least 2")

        if any(x < 0 or x >= base for x in integer_part):
            raise BasesValueError(
                integer_part,
                "integer_part",
                "for all elements, e, 0 <= e < base required",
            )

        if any(x < 0 or x >= base for x in non_repeating_part):
            raise BasesValueError(
                non_repeating_part,
                "non_repeating_part",
                "for all elements, e, 0 <= e < base required",
            )

        if any(x < 0 or x >= base for x in repeating_part):
            raise BasesValueError(
                repeating_part,
                "repeating_part",
                "for all elements, e, 0 <= e < base required",
            )

        shift_length = len(repeating_part)
        frac_length = len(non_repeating_part)

        top = fractions.Fraction(
            Nats.convert_to_int(
                integer_part + non_repeating_part + repeating_part, base
            ),
            base ** frac_length,
        )

        if shift_length == 0:
            return (
                Nats.convert_from_int(top.denominator, base),
                Nats.convert_from_int(top.numerator, base),
            )

        bottom = fractions.Fraction(
            Nats.convert_to_int(integer_part + non_repeating_part, base),
            base ** frac_length,
        )
        result = (top - bottom) / ((base ** shift_length) - 1)
        return (
            Nats.convert_from_int(result.denominator, base),
            Nats.convert_from_int(result.numerator, base),
        )
